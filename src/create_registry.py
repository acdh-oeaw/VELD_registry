import os
from time import sleep

import yaml
import requests


GITHUB_TOKEN = os.getenv("github_token")
GITLAB_TOKEN = os.getenv("gitlab_token")


def crawl_repo_github(repo_url, path, veld_list):
    response = requests.get(url=repo_url + "/" + path, headers={"Authorization": f"token {GITHUB_TOKEN}"})
    response_dict_list = response.json()
    for item_dict in response_dict_list:
        item_type = item_dict["type"]
        item_path = item_dict["path"]
        if item_type == "file":
            item_file_name = item_path.split("/")[-1]
            if item_file_name.startswith("veld") and item_file_name.endswith(".yaml"):
                veld_list.append(item_path)
        elif item_type == "dir":
            crawl_repo_github(repo_url, item_path, veld_list)
    return veld_list


def crawl_repo_gitlab(repo_url, path, veld_list):
    page = "1"
    while page != "":
        response = requests.get(
            url=repo_url, 
            headers={"PRIVATE-TOKEN": GITLAB_TOKEN},
            params={"path": path, "page": page}
        )
        response_dict_list = response.json()
        for item_dict in response_dict_list:
            item_type = item_dict["type"]
            item_path = item_dict["path"]
            if item_type == "blob":
                item_file_name = item_path.split("/")[-1]
                if item_file_name.startswith("veld") and item_file_name.endswith(".yaml"):
                    veld_list.append(item_path)
            elif item_type == "tree":
                crawl_repo_gitlab(repo_url, item_path, veld_list)
        page = response.headers.get("X-Next-Page")
    return veld_list


def process_links():
    content = ""
    with open("README.md", "r") as f:
        for line in f:
            if not line.startswith("  -"):
                content += line
            if line.startswith("- http"):
                repo_url = line[2:-1]
                if "github.com" in repo_url:
                    repo_api_url = repo_url.replace(
                        "https://github.com/", "https://api.github.com/repos/"
                    )
                    repo_api_url += "/contents/"
                    veld_list = crawl_repo_github(repo_api_url, "", [])
                elif "gitlab.oeaw.ac.at" in repo_url:
                    repo_api_url = repo_url.replace("https://gitlab.oeaw.ac.at/", "")
                    repo_api_url = repo_api_url.replace("/", "%2F")
                    repo_api_url = "https://gitlab.oeaw.ac.at/api/v4/projects/" + repo_api_url + \
                        "/repository/tree"
                    veld_list = crawl_repo_gitlab(repo_api_url, "", [])
                print(line)
                print(veld_list)
                for veld in veld_list:
                    veld_url = repo_url + "/blob/main/" + veld
                    content += f"  - [{veld}]({veld_url})\n"

    with open("README.md", "w") as f:
        f.write(content)


def main():
    process_links()


if __name__ == "__main__":
    main()

