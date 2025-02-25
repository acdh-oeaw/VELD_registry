import base64
import math
import os

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


def crawl_repo_github(repo_api_url, path, veld_list):
    response = requests.get(
        url=repo_api_url + "/" + path,
        headers={"Authorization": f"token {GITHUB_TOKEN}"}
    )
    if response.status_code != 200:
        raise Exception("Not 200 status: " + str(response.content))
    response = response.json()
    for item_dict in response:
        item_type = item_dict["type"]
        item_path = item_dict["path"]
        if item_type == "file":
            item_file_name = item_path.split("/")[-1]
            if item_file_name.startswith("veld") and item_file_name.endswith(".yaml"):
                response = requests.get(
                    url=repo_api_url + item_path,
                    headers={"Authorization": f"token {GITHUB_TOKEN}"}
                )
                response = response.json()
                item_content = base64.b64decode(response["content"]).decode("utf-8")
                if item_content != "":
                    validation_result, metadata = validate_metadata(item_content)
                    veld_list.append({
                        "path": item_path,
                        "item_content": item_content,
                        "validation_result": validation_result,
                        "metadata": metadata,
                    })
        elif item_type == "dir":
            crawl_repo_github(repo_api_url, item_path, veld_list)
    return veld_list


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


def handle_metadata(veld, level):
    content = ""
    md = veld.get("metadata")
    md = md.get("x-veld")
    if md is not None:
        md = list(md.values())[0]
        if md is not None:
            for k in ["description", "topic", "file_type", "content"]:
                v = md.get(k)
                if v is not None:
                    add_to_set(k, v)
                    content += transform_dict(k, v, level + 2)
            for k in ["input", "output"]:
                v = md.get(k)
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


def crawl_all(link_txt_path, all_velds):
    content = ""
    test_count_gh = 0
    test_count_gl = 0
    limit = math.inf
    with open(link_txt_path, "r") as f:
        for repo_url in f.read().splitlines():
            content += "- " + repo_url + "\n"
            print("crawling repo url:", repo_url)
            veld_list = []
            if "github.com" in repo_url and test_count_gh < limit:
                repo_api_url = repo_url.replace(
                    "https://github.com/", "https://api.github.com/repos/"
                )
                repo_api_url += "/contents/"
                veld_list = crawl_repo_github(repo_api_url, "", [])
                test_count_gh += 1
            elif "gitlab.oeaw.ac.at" in repo_url and test_count_gh < limit:
                repo_api_url = repo_url.replace("https://gitlab.oeaw.ac.at/", "")
                repo_api_url = repo_api_url.replace("/", "%2F")
                repo_api_url = "https://gitlab.oeaw.ac.at/api/v4/projects/" + repo_api_url + "/repository"
                veld_list = crawl_repo_gitlab(repo_api_url, "", [])
                test_count_gl += 1
            for veld in veld_list:
                out_veld_id = repo_url.split("/")[-1] + "___" + veld["path"].replace("/", "___")
                with open(OUT_VELD_INDIVIDUAL_FOLDER + out_veld_id, "w") as f_out:
                    f_out.write(veld["item_content"])
                veld_url = repo_url + "/blob/main/" + veld["path"]
                print("found veld url:", veld_url)
                print(f"valid: {veld['validation_result'][0]}")
                content += f"  - [{veld['path']}]({veld_url})\n"
                if veld["validation_result"][0]:
                    validate_message = "True"
                else:
                    validate_message = "False, " + veld["validation_result"][1]
                content += f"    - valid: {validate_message}\n"
                if veld["validation_result"][0]:
                    all_velds[out_veld_id] = {"url": veld_url, "content": veld["metadata"]}
                    content_md = handle_metadata(veld, 4)
                    if content_md != "":
                        content += f"    - metadata:\n"
                        content += content_md
    return content, all_velds


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
    content = ""
    all_velds = {}
    content += "\n## data velds\n"
    content_tmp, all_velds = crawl_all(IN_LINKS_DATA_PATH, all_velds)
    content += content_tmp
    content += "\n## code velds\n"
    content_tmp, all_velds = crawl_all(IN_LINKS_CODE_PATH, all_velds)
    content += content_tmp
    content += "\n## chain velds\n"
    content_tmp, all_velds = crawl_all(IN_LINKS_CHAIN_PATH, all_velds)
    content += content_tmp

    # sets
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
    with open(OUT_VELD_MERGED_PATH, "w", encoding="utf-8") as f_out:
        yaml.dump(all_velds, f_out, sort_keys=False)


if __name__ == "__main__":
    main()

