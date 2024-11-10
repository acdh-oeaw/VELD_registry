import types

import yaml


IN_VELD_DATA_PATH = "/app/data/veld_files/merged/all_velds_merged.yaml"


with open(IN_VELD_DATA_PATH, "r") as f:
    VELD_DATA_ALL = yaml.safe_load(f)


def _get_veld_by_type(veld_type):
    result = {}
    for k, v in VELD_DATA_ALL.items():
        try:
            _ = v["content"]["x-veld"][veld_type]
            url = v["url"]
        except KeyError:
            pass
        else:
            result[k] = [url]
    return result


def get_data_veld_instances():
    result = _get_veld_by_type("data")
    return result


def get_code_veld_instances():
    result = _get_veld_by_type("code")
    return result


def get_chain_veld_instances():
    result = _get_veld_by_type("chain")
    return result


def get_code_reification_to_topic():
    result = {}
    i = 1
    for k, v in VELD_DATA_ALL.items():
        try:
            _ = v["content"]["x-veld"]["code"]
            topics = v["content"]["x-veld"]["code"]["topics"]
            url = v["url"]
            if topics == "" or topics == [] or topics is None:
                raise Exception
        except:
            pass
        else:
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
            url = v["url"]
            if topics == "" or topics == [] or topics is None:
                raise Exception
            if type(topics) is str:
                topics = [topics]
        except:
            pass
        else:
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
            inputs = []
            for input_group in input_group_list:
                input_group_file_type = input_group["file_type"]
                if type(input_group_file_type) is list:
                    for ft in input_group_file_type:
                        inputs.append(ft)
                elif type(input_group_file_type) is str:
                    inputs.append(input_group_file_type)
            if inputs == [] or inputs is None:
                raise Exception
        except:
            pass
        else:
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
            for s in v["content"]["services"].values():
                code_veld_file = s["extends"]["file"]
                code_veld_id = code_veld_file[2:].replace("/", "__")
                code_veld_instances = get_code_veld_instances()
                code_veld_url = code_veld_instances[code_veld_id]
        except:
            pass
        else:
            if code_veld_url is not None:
                result[k] = code_veld_url
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
