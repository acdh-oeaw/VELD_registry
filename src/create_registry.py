import base64
import math
import os
from dataclasses import dataclass, field

import yaml
import requests
from veld_spec import validate


GITHUB_TOKEN = os.getenv("github_token")
GITLAB_TOKEN = os.getenv("gitlab_token")
IN_LINKS_DATA_PATH = "/app/data/links_repos/links_data_velds.txt"
IN_LINKS_CODE_PATH = "/app/data/links_repos/links_code_velds.txt"
IN_LINKS_CHAIN_PATH = "/app/data/links_repos/links_chain_velds.txt"
IN_README_TEMPLATE_PATH = "/app/data/veldhub_meta_repo/profile/README_template.md"
OUT_README_PATH_REGISTRY = "/app/README.md"
OUT_README_PATH_VELHDUB = "/app/data/veldhub_meta_repo/profile/README.md"
OUT_VELD_INDIVIDUAL_FOLDER = "/app/data/veld_files/individual/"
OUT_VELD_MERGED_PATH = "/app/data/veld_files/merged/all_velds_merged.yaml"


set_topic = set()
set_file_type = set()
set_content = set()


@dataclass
class VeldRepresentation():
    url_repo: str = None
    url_veld_yaml: str = None
    path_relative: str = None
    content_str: str = None
    content_dict: dict = None
    is_valid: bool = None
    validation_message: str = None
    veld_type: str = None
    contains_code: list = field(default_factory=list)
    contains_input: list = field(default_factory=list)
    contains_output: list = field(default_factory=list)
    is_code_of: list = field(default_factory=list)
    is_input_of: list = field(default_factory=list)
    is_output_of: list = field(default_factory=list)
    
    
def get_veld_type(metadata):
    type = None
    try:
        type = list(metadata["x-veld"].keys())[0]
    except:
        pass
    return type

    
def validate_metadata(veld_metadata_str):
    try:
        veld_metadata = yaml.safe_load(veld_metadata_str)
        if veld_metadata is not None:
            validation_result = validate(dict_to_validate=veld_metadata)
        else:
            validation_result = (False, "empty yaml")
            veld_metadata = None
    except:
        validation_result = (False, "broken yaml")
        veld_metadata = None
    return validation_result, veld_metadata
    
    
def normalize_submodule_path(path):
    if path.startswith("./"):
        path = path[2:]
    if path.endswith("/"):
        path = path[:-1]
    return path


def get_contained_velds_of_chain(veld, gitmodules_dict):
    service_dict_list = veld.content_dict.get("services", [])
    for service_dict in service_dict_list.values():
        service_extends = service_dict.get("extends")
        if service_extends:
            service_extends_path = service_extends.get("file")
            if service_extends_path:
                service_extends_path = normalize_submodule_path(service_extends_path)
                for gitmodule_path, gitmodule_url in gitmodules_dict.items():
                    if gitmodule_path in service_extends_path:
                        if gitmodule_url not in veld.contains_code:
                            veld.contains_code.append(gitmodule_url)
        volume_list = service_dict.get("volumes", [])
        for volume in volume_list:
            volume_host, volume_container = volume.split(":")[:2]
            if volume_host:
                volume_host = normalize_submodule_path(volume_host)
                for gitmodule_path, gitmodule_url in gitmodules_dict.items():
                    if gitmodule_path in volume_host:
                        if volume_container.startswith("/veld/input"):
                            if gitmodule_url not in veld.contains_input:
                                veld.contains_input.append(gitmodule_url)
                        elif volume_container.startswith("/veld/output"):
                            if gitmodule_url not in veld.contains_output:
                                veld.contains_output.append(gitmodule_url)
    return veld


def get_submodule_content(repo_api_url):
    gitmodules_dict = None
    gitmodules_response = get_from_repo_path(repo_api_url, ".gitmodules")
    if gitmodules_response.status_code == 200:
        gitmodules_dict = {}
        gitmodules_str = base64.b64decode(gitmodules_response.json()["content"]).decode("utf-8")
        path = None
        url = None
        for line in gitmodules_str.splitlines():
            if not line.startswith("["):
                path_split = line.split("	path = ")
                if len(path_split) == 2:
                    path = path_split[1]
                    path = normalize_submodule_path(path)
                url_split = line.split("	url = ")
                if len(url_split) == 2:
                    url = url_split[1].replace(".git", "")
            if path and url:
                gitmodules_dict[path] = url
                path = None
                url = None
    return gitmodules_dict


def get_from_repo_path(repo_api_url, path):
    return requests.get(
        url=repo_api_url + "/" + path,
        headers={"Authorization": f"token {GITHUB_TOKEN}"}
    )
    

def crawl_repo_github_recursively(repo_api_url, path, veld_list, gitmodules_dict):
    response = get_from_repo_path(repo_api_url, path)
    if response.status_code != 200:
        raise Exception("Not 200 status: " + str(response.content))
    response = response.json()
    for item_dict in response:
        item_type = item_dict["type"]
        item_path = item_dict["path"]
        if item_type == "file":
            item_file_name = item_path.split("/")[-1]
            if item_file_name.startswith("veld") and item_file_name.endswith(".yaml"):
                response = get_from_repo_path(repo_api_url, item_path)
                response = response.json()
                item_content = base64.b64decode(response["content"]).decode("utf-8")
                if item_content != "":
                    validation_result, metadata = validate_metadata(item_content)
                    veld = VeldRepresentation(
                        path_relative=item_path,
                        is_valid=validation_result[0],
                        validation_message=validation_result[1],
                        content_dict=metadata,
                        content_str=item_content,
                        veld_type=get_veld_type(metadata),
                    )
                    if veld.veld_type == "chain":
                        veld = get_contained_velds_of_chain(veld, gitmodules_dict)
                    veld_list.append(veld)
        elif item_type == "dir":
            crawl_repo_github_recursively(repo_api_url, item_path, veld_list, gitmodules_dict)
    return veld_list


def crawl_repo_github(repo_api_url, path, veld_list):
    gitmodules_dict = get_submodule_content(repo_api_url)
    return crawl_repo_github_recursively(repo_api_url, path, veld_list, gitmodules_dict)
    

def crawl_repo_gitlab(repo_api_url, path, veld_list):
    page = "1"
    while page != "":
        response = requests.get(
            url=repo_api_url + "/tree",
            headers={"PRIVATE-TOKEN": GITLAB_TOKEN},
            params={"path": path, "page": page}
        )
        if response.status_code != 200:
            raise Exception("Not 200 status: " + str(response.content))
        page = response.headers.get("X-Next-Page")
        response = response.json()
        for item_dict in response:
            item_type = item_dict["type"]
            item_path = item_dict["path"]
            if item_type == "blob":
                item_file_name = item_path.split("/")[-1]
                if item_file_name.startswith("veld") and item_file_name.endswith(".yaml"):
                    response = requests.get(
                        url=repo_api_url + f"/files/{item_path}/raw",
                        headers={"PRIVATE-TOKEN": GITLAB_TOKEN},
                    )
                    item_content = response.text
                    if item_content != "" and item_content != '{"error":"404 Not Found"}':
                        validation_result, metadata = validate_metadata(item_content)
                        veld_list.append({
                            "path": item_path,
                            "item_content": item_content,
                            "validation_result": validation_result,
                            "metadata": metadata,
                        })
            elif item_type == "tree":
                crawl_repo_gitlab(repo_api_url, item_path, veld_list)
    return veld_list


def create_md_string(k, v, level):
    s = ""
    if k != "":
        k = k + ": "
    if type(v) is list:
        v = ", ".join(v)
    v = str(v)
    if v != "" and not v.isspace():
        s = " " * level + "- " + k + v + "\n"
    return s


def transform_dict(k, v, level):
    s = ""
    if type(v) is not dict:
        s += create_md_string(k, v, level)
    else:
        s += create_md_string("", k + ":", level)
        for k2, v2 in v.items():
            s += transform_dict(k2, v2, level + 2)
    return s


def add_to_set(k, v):
    
    def add_to_specific_set(v, s):
        if type(v) is not list:
            v = [v]
        for v2 in v:
            s.add(v2)
    
    if k == "topic":
        add_to_specific_set(v, set_topic)
    elif k == "content":
        add_to_specific_set(v, set_content)
    elif k == "file_type":
        add_to_specific_set(v, set_file_type)


def handle_metadata(metadata, level):
    content = ""
    metadata = metadata.get("x-veld")
    if metadata:
        metadata = list(metadata.values())[0]
        if metadata is not None:
            for k in ["description", "topic", "file_type", "content"]:
                v = metadata.get(k)
                if v is not None:
                    add_to_set(k, v)
                    content += transform_dict(k, v, level + 2)
            for k in ["input", "output"]:
                v = metadata.get(k)
                if type(v) is list:
                    for i, d in enumerate(v):
                        if i == 0:
                            content += create_md_string("", k + ":", level + 2)
                        content += create_md_string("", str(i + 1) + ":", level + 4)
                        for k2 in ["description", "file_type", "content"]:
                            v2 = d.get(k2)
                            if v2 is not None:
                                add_to_set(k2, v2)
                                content += create_md_string(k2, v2, level + 6)
    return content


def crawl_all(link_txt_path, veld_dict_all):
    test_count_gh = 0
    test_count_gl = 0
    limit = math.inf
    with open(link_txt_path, "r") as f:
        for url_repo in f.read().splitlines():
            print("crawling repo url:", url_repo)
            veld_list_pre_repo = []
            if "github.com" in url_repo and test_count_gh < limit:
                repo_api_url = url_repo.replace(
                    "https://github.com/", "https://api.github.com/repos/"
                )
                repo_api_url += "/contents/"
                veld_list_pre_repo = crawl_repo_github(repo_api_url, "", [])
                test_count_gh += 1
            elif "gitlab.oeaw.ac.at" in url_repo and test_count_gh < limit:
                repo_api_url = url_repo.replace("https://gitlab.oeaw.ac.at/", "")
                repo_api_url = repo_api_url.replace("/", "%2F")
                repo_api_url = "https://gitlab.oeaw.ac.at/api/v4/projects/" + repo_api_url + "/repository"
                veld_list_pre_repo = crawl_repo_gitlab(repo_api_url, "", [])
                test_count_gl += 1
            for veld in veld_list_pre_repo:
                url_veld_yaml = url_repo + "/blob/main/" + veld.path_relative
                veld_id = url_repo.split("/")[-1] + "___" + veld.path_relative.replace("/", "___")
                veld.url_veld_yaml = url_veld_yaml
                veld.url_repo = url_repo
                print("found veld url:", url_veld_yaml)
                print(f"valid: {veld.is_valid}")
                veld_dict_all[veld_id] = veld
    return veld_dict_all


def link_contained_velds(veld_dict_all):
    for veld_key, veld_chain in veld_dict_all.items():
        for veld_other in veld_dict_all.values():
            if veld_chain.veld_type == "chain":
                for contained_code_url in veld_chain.contains_code:
                    if veld_other.url_repo == contained_code_url and veld_chain.url_repo not in veld_other.is_code_of:
                        veld_other.is_code_of.append(veld_chain.url_repo)
                for contained_input_url in veld_chain.contains_input:
                    if veld_other.url_repo == contained_input_url and veld_chain.url_repo not in veld_other.is_input_of:
                        veld_other.is_input_of.append(veld_chain.url_repo)
                for contained_output_url in veld_chain.contains_output:
                    if veld_other.url_repo == contained_output_url and veld_chain.url_repo not in veld_other.is_output_of:
                        veld_other.is_output_of.append(veld_chain.url_repo)
    return veld_dict_all


def convert_to_readme_section_individual(veld_dict_all, veld_type):
    content = ""
    
    veld_dict_by_repo = {}
    for veld_key, veld in veld_dict_all.items():
        if veld.veld_type == veld_type:
            contained_velds = veld_dict_by_repo.get(veld.url_repo, [])
            contained_velds.append(veld)
            veld_dict_by_repo[veld.url_repo] = contained_velds
            
    for url_repo, veld_list in veld_dict_by_repo.items():
        content += "- " + url_repo + "\n"
        for veld in veld_list:
            veld: VeldRepresentation
            content += f"  - [{veld.path_relative}]({veld.url_veld_yaml})\n"
            if veld.is_valid:
                content += f"    - valid: {veld.is_valid}\n"
            else:
                content += f"    - valid: {veld.is_valid}, {veld.validation_message}\n"
            if veld.veld_type == "chain":
                if veld.contains_code:
                    content += f"    - contains code velds:\n"
                    for contained_veld_url in veld.contains_code:
                        content += f"      - {contained_veld_url}\n"
                if veld.contains_input:
                    content += f"    - contains input velds:\n"
                    for contained_veld_url in veld.contains_input:
                        content += f"      - {contained_veld_url}\n"
                if veld.contains_output:
                    content += f"    - contains output velds:\n"
                    for contained_veld_url in veld.contains_output:
                        content += f"      - {contained_veld_url}\n"
            else:
                if veld.is_code_of:
                    content += f"    - is contained as code veld in:\n"
                    for chain_veld_url in veld.is_code_of:
                        content += f"      - {chain_veld_url}\n"
                if veld.is_input_of:
                    content += f"    - is contained as input veld in:\n"
                    for chain_veld_url in veld.is_input_of:
                        content += f"      - {chain_veld_url}\n"
                if veld.is_output_of:
                    content += f"    - is contained as output veld in:\n"
                    for chain_veld_url in veld.is_output_of:
                        content += f"      - {chain_veld_url}\n"
            if veld.is_valid:
                content_md = handle_metadata(veld.content_dict, 4)
                if content_md != "":
                    content += f"    - metadata:\n"
                    content += content_md
    return content


def convert_to_readme_section(veld_dict_all):
    content = ""
    content += "\n## data velds\n"
    content += convert_to_readme_section_individual(veld_dict_all, "data")
    content += "\n## code velds\n"
    content += convert_to_readme_section_individual(veld_dict_all, "code")
    content += "\n## chain velds\n"
    content += convert_to_readme_section_individual(veld_dict_all, "chain")
    return content


def main():
    
    # delete all veld output
    if os.path.exists(OUT_README_PATH_REGISTRY):
        os.remove(OUT_README_PATH_REGISTRY)
    if os.path.exists(OUT_README_PATH_VELHDUB):
        os.remove(OUT_README_PATH_VELHDUB)
    if os.path.exists(OUT_VELD_MERGED_PATH):
        os.remove(OUT_VELD_MERGED_PATH)
    if os.path.exists(OUT_VELD_INDIVIDUAL_FOLDER):
        for f in os.listdir(OUT_VELD_INDIVIDUAL_FOLDER):
            os.remove(OUT_VELD_INDIVIDUAL_FOLDER + "/" + f)
            
    # README header
    content_prefix_registry = (
        "# VELD registry\n\n"
        "This is a living collection of VELD repositories and their contained velds.\n\n"
        "The technical concept for the VELD design can be found here: "
        "https://zenodo.org/records/13318651\n\n"
        "#### sections in this README:\n"
        "[data velds](#data-velds)\n\n"
        "[code velds](#code-velds)\n\n"
        "[chain velds](#chain-velds)\n\n"
        "[topic vocab](#topic-vocab)\n\n"
        "[content vocab](#content-vocab)\n\n"
        "[file_type vocab](#file_type-vocab)\n\n"
    )
    with open(IN_README_TEMPLATE_PATH, "r") as f:
        content_prefix_veldhub = f.read()
    
    # crawl over all links
    veld_dict_all = {}
    veld_dict_all = crawl_all(IN_LINKS_CHAIN_PATH, veld_dict_all)
    veld_dict_all = crawl_all(IN_LINKS_DATA_PATH, veld_dict_all)
    veld_dict_all = crawl_all(IN_LINKS_CODE_PATH, veld_dict_all)
    veld_dict_all = link_contained_velds(veld_dict_all)
    
    # create readme content
    content = convert_to_readme_section(veld_dict_all)
    content += "\n## topic vocab\n"
    list_vocab = list(set_topic)
    list_vocab = sorted(list_vocab, key=str.casefold)
    for s in list_vocab:
        content += "- " + s + "\n"
    content += "\n## content vocab\n"
    list_vocab = list(set_content)
    list_vocab = sorted(list_vocab, key=str.casefold)
    for s in list_vocab:
        content += "- " + s + "\n"
    content += "\n## file_type vocab\n"
    list_vocab = list(set_file_type)
    list_vocab = sorted(list_vocab, key=str.casefold)
    for s in list_vocab:
        content += "- " + s + "\n"

    # write
    content_registry = content_prefix_registry + content
    content_veldhub = content_prefix_veldhub + content
    with open(OUT_README_PATH_REGISTRY, "w") as f:
        f.write(content_registry)
    with open(OUT_README_PATH_VELHDUB, "w") as f:
        f.write(content_veldhub)
    for veld_id, veld in veld_dict_all.items():
        with open(OUT_VELD_INDIVIDUAL_FOLDER + veld_id, "w") as f_out:
            f_out.write(veld.content_str)
    veld_metadata_only = {}
    for veld_id, veld in veld_dict_all.items():
        veld_metadata_only[veld_id] = {
            "url": veld.url_veld_yaml,
            "content": veld.content_dict,
        }
    with open(OUT_VELD_MERGED_PATH, "w", encoding="utf-8") as f_out:
        yaml.dump(veld_metadata_only, f_out, sort_keys=False)


if __name__ == "__main__":
    main()
