import types

import yaml


IN_VELD_DATA_PATH = "/app/data/veld_files/merged/all_velds_merged.yaml"


with open(IN_VELD_DATA_PATH, "r") as f:
    VELD_DATA_ALL = yaml.safe_load(f)


def _get_veld_uri_by_type(veld_type):
    result = {}
    for k, v in VELD_DATA_ALL.items():
        try:
            _ = v["content"]["x-veld"][veld_type]
            _ = v["url"]
        except KeyError:
            continue
        else:
            result[k] = [v["url"]]
    return result


def get_data_veld_uris():
    result = _get_veld_uri_by_type("data")
    return result


def get_data_veld_uris__as_chain_input():
    result = {}
    i = 1
    for k, v in VELD_DATA_ALL.items():
        try:
            _ = v["content"]["x-veld"]["chain"]
            services = v["content"]["services"]
            volumes_list = []
            for s in services.values():
                for v in s.get("volumes"):
                    volumes_list.append(v)
        except:
            continue
        else:
            result[k] = [f"clscor:/code_reification_to_topic_{i}"]
            i += 1
    return result


def get_code_veld_uris():
    result = _get_veld_uri_by_type("code")
    return result


def get_chain_veld_uris():
    result = _get_veld_uri_by_type("chain")
    return result


def get_code_reification_to_topic():
    result = {}
    i = 1
    for k, v in VELD_DATA_ALL.items():
        try:
            _ = v["content"]["x-veld"]["code"]
            topics = v["content"]["x-veld"]["code"]["topics"]
        except:
            continue
        else:
            if topics != "" and topics != [] and topics is not None:
                result[k] = [f"clscor:/code_reification_to_topic_{i}"]
                i += 1
    return result


def get_topic_of_code_reification_to_topic():
    result = {}
    i = 1
    for k, v in VELD_DATA_ALL.items():
        try:
            _ = v["content"]["x-veld"]["code"]
            topics = v["content"]["x-veld"]["code"]["topics"]
        except:
            continue
        else:
            if type(topics) is str and topics != "":
                topics = [topics]
            if topics != [] and topics is not None:
                result[k] = topics
                i += 1
    return result


def get_code_input_file_type():
    result = {}
    i = 1
    for k, v in VELD_DATA_ALL.items():
        try:
            _ = v["content"]["x-veld"]["code"]
            input_group_list = v["content"]["x-veld"]["code"]["inputs"]
        except:
            continue
        else:
            inputs = []
            for input_group in input_group_list:
                input_group_file_type = input_group["file_type"]
                if type(input_group_file_type) is list:
                    for ft in input_group_file_type:
                        inputs.append(ft)
                elif type(input_group_file_type) is str:
                    inputs.append(input_group_file_type)
            if inputs != [] and inputs is not None:
                result[k] = inputs
                i += 1
    return result


def get_integrated_code_veld_id():
    result = {}
    i = 1
    for k, v in VELD_DATA_ALL.items():
        code_veld_url = None
        try:
            _ = v["content"]["x-veld"]["chain"]
            services = v["content"]["services"]
            code_veld_file_list = [s["extends"]["file"] for s in services.values()]
        except:
            continue
        else:
            code_veld_url_list = []
            for code_veld_file in code_veld_file_list:
                code_veld_id = code_veld_file[2:].replace("/", "__")
                code_veld_instances = get_code_veld_uris()
                code_veld_url = code_veld_instances.get(code_veld_id)
                if code_veld_url is not None:
                    code_veld_url_list.append(code_veld_url)
            if code_veld_url_list != []:
                result[k] = code_veld_url_list
                i += 1
    return result


def do_scopes_align(k1, k2, k3):
    
    def do_two_align(k1, k2):
        result = (k1 is None or k2 is None) or (k1 == k2)
        return result
    
    result = do_two_align(k1, k2) and do_two_align(k1, k3) and do_two_align(k2, k3)
    return result


def main():
    from data.clscor_conversion.mapping import mappings
    
    for m_id, m in mappings.items():
        m_instantiated = {}
        for k, v in m.items():
            if type(v) is types.FunctionType:
                m_instantiated[k] = v()
            else:
                m_instantiated[k] = {None: [v]}
        for s_scope, s_list in m_instantiated["s"].items():
            for p_scope, p_list in m_instantiated["p"].items():
                for o_scope, o_list in m_instantiated["o"].items():
                    if do_scopes_align(s_scope, p_scope, o_scope):
                        for s in s_list:
                            for p in p_list:
                                for o in o_list:
                                    print(s, p, o)
                                    

if __name__ == "__main__":
    main()
