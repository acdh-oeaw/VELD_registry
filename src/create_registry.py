import base64
import os

import yaml
import requests
from veld_spec import validate

from datetime import datetime


GITHUB_TOKEN = os.getenv("github_token")
GITLAB_TOKEN = os.getenv("gitlab_token")
README_PATH = "/app/out/README.md"
TXT_PATH_CHAIN_VELDS = "/app/in/links_chain_velds.txt"
TXT_PATH_CODE_VELDS = "/app/in/links_code_velds.txt"
TXT_PATH_DATA_VELDS = "/app/in/links_data_velds.txt"


def validate_metadata(veld_metadata_str):
    veld_metadata = yaml.safe_load(veld_metadata_str)
    if veld_metadata is not None:
        validation_result = validate(dict_to_validate=veld_metadata)
        if validation_result[0]:
            validation_message = "True"
        else:
            validation_message = "False, " + validation_result[1]
    else:
        validation_message = "False, " + "broken yaml or empty"
    return validation_message


def crawl_repo_github(repo_api_url, path, veld_list):
    response = requests.get(
        url=repo_api_url + "/" + path,
        headers={"Authorization": f"token {GITHUB_TOKEN}"}
    )
    response_dict_list = response.json()
    for item_dict in response_dict_list:
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
                    validation_message = validate_metadata(item_content)
                    veld_list.append({
                        "path": item_path,
                        "valid": validation_message,
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
        page = response.headers.get("X-Next-Page")
        response_dict_list = response.json()
        for item_dict in response_dict_list:
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
                    if item_content != "":
                        validation_message = validate_metadata(item_content)
                        veld_list.append({
                            "path": item_path,
                            "valid": validation_message,
                        })
            elif item_type == "tree":
                crawl_repo_gitlab(repo_api_url, item_path, veld_list)
    return veld_list


def generate_list(link_txt_path):
    content = ""
    with open(link_txt_path, "r") as f:
        for line in f:
            content += "- " + line
            repo_url = line[:-1]
            print(repo_url)
            if "github.com" in repo_url:
                repo_api_url = repo_url.replace(
                    "https://github.com/", "https://api.github.com/repos/"
                )
                repo_api_url += "/contents/"
                veld_list = crawl_repo_github(repo_api_url, "", [])
            elif "gitlab.oeaw.ac.at" in repo_url:
                repo_api_url = repo_url.replace("https://gitlab.oeaw.ac.at/", "")
                repo_api_url = repo_api_url.replace("/", "%2F")
                repo_api_url = "https://gitlab.oeaw.ac.at/api/v4/projects/" + repo_api_url + "/repository"
                veld_list = crawl_repo_gitlab(repo_api_url, "", [])
            print(veld_list)
            for veld in veld_list:
                veld_url = repo_url + "/blob/main/" + veld["path"]
                content += f"  - [{veld['path']}]({veld_url})\n"
                content += f"    - valid: {veld['valid']}\n"
    return content


def main():
    content = (
        "# VELD registry\n\n"
        "This is a living collection of VELD repositories and their contained velds.\n\n"
        "The technical concept for the VELD design can be found here: "
        "https://zenodo.org/records/13318651\n\n"
    )
    content += "\n## chain velds\n"
    content += generate_list(TXT_PATH_CHAIN_VELDS)
    content += "\n## code velds\n"
    content += generate_list(TXT_PATH_CODE_VELDS)
    content += "\n## data velds\n"
    content += generate_list(TXT_PATH_DATA_VELDS)
    with open(README_PATH, "w") as f:
        f.write(content)


if __name__ == "__main__":
    main()

