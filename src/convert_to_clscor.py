import yaml


IN_MAPPING_PATH = "/app/data/clscor_conversion/mapping.yaml"
IN_VELD_MERGED_PATH = "/app/data/veld_files/merged/all_velds_merged.yaml"


def main():
    with open(IN_MAPPING_PATH, "r") as f_in:
        mapping = yaml.safe_load(f_in)
    
    with open(IN_VELD_MERGED_PATH, "r") as f_in:
        all_velds = yaml.safe_load(f_in)
        for veld_url_content in all_velds.values():
            veld_url = veld_url_content["url"]
            veld_content = veld_url_content["content"]


if __name__ == "__main__":
    main()
