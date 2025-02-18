import hashlib
import types

import yaml

from data.clscor_conversion.rdf_modules_namespaces import *
from data.clscor_conversion import mapping


IN_VELD_DATA_PATH = "/app/data/veld_files/merged/all_velds_merged.yaml"
with open(IN_VELD_DATA_PATH, "r") as f:
    VELD_DATA_ALL = yaml.safe_load(f)
OUT_TTL_DATA_PATH = "/app/data/clscor_conversion/output.ttl"


def _generate_hash(s):
    return hashlib.sha256(s.encode()).hexdigest()[:10]


def _get_data_recursively(d, key_list):
    if type(d) is dict and key_list and key_list[0] in d:
        d_val = d[key_list[0]]
        return _get_data_recursively(d_val, key_list[1:])
    elif len(key_list) == 0:
        if d is None:
            d = []
        return d
    else:
        return None
    

def _get_veld_uri_by_type(veld_data, veld_type):
    result = []
    result_veld_type = _get_data_recursively(veld_data, ["content", "x-veld", veld_type])
    if result_veld_type is not None:
        result_url = _get_data_recursively(veld_data, ["url"])
        if result_url:
            result = [URIRef(veld_data["url"])]
    return result


def _get_veld_label(veld_data):
    result = []
    veld_url = veld_data.get("url")
    if veld_url is not None:
        url_part_list = veld_url.split("https://github.com/veldhub/")[1].split("/")
        label_repo = url_part_list[0]
        label_veld = url_part_list[-1].split(".yaml")[0]
        if label_veld == "veld":
            label = label_repo
        else:
            label = label_repo + "__" + label_veld.replace("veld_", "")
        result = [Literal(label)]
    return result


def _get_data_veld_uris__as_chain_io(veld_data, io):
    result = []
    volumes_list = []
    if _get_data_recursively(veld_data, ["content", "x-veld", "chain"]) is not None:
        services = _get_data_recursively(veld_data, ["content", "services"])
        for s in services.values():
            v = s.get("volumes")
            if v is not None:
                for vol in v:
                    volumes_list.append(vol)
    if volumes_list:
        data_veld_uris = {}
        for data_veld_id, data_veld_data in VELD_DATA_ALL.items():
            if _get_data_recursively(data_veld_data, ["content", "x-veld", "data"]) is not None:
                data_veld_uris[data_veld_id] = data_veld_data["url"]
        for vol in volumes_list:
            vol = vol.split(":")
            if io in vol[1]:
                chain_data_path = vol[0][2:]
                chain_data_path = chain_data_path.split("/")
                match_count_max = 0
                for data_id, data_uri in data_veld_uris.items():
                    data_id = data_id.split("___")
                    match_count_tmp = 0
                    for i in range(min(len(chain_data_path), len(data_id))):
                        if chain_data_path[i] == data_id[i]:
                            match_count_tmp += 1
                    if match_count_tmp > match_count_max:
                        match_count_max = match_count_tmp
                        if match_count_max > 0:
                            result.append(URIRef(data_uri))
    return result


def _get_code_ved__file_type__of_io(veld_data, io_direction):
    result = []
    io = _get_data_recursively(veld_data, ["content", "x-veld", "code", io_direction])
    if io is not None:
        if type(io) is dict:
            io = [io]
        for io_dict in io:
            if ft := io_dict.get("file_type"):
                result.extend(_transform_file_type(ft))
    return result


def _check_if_type(veld_data, veld_type):
    result = _get_data_recursively(veld_data, ["content", "x-veld", veld_type])
    return result is not None


def _get_topic(veld_data):
    result = []
    veld_data_any = _get_data_recursively(veld_data, ["content", "x-veld"])
    if veld_data_any is not None:
        topics = list(veld_data_any.values())[0].get("topic")
        if type(topics) is str:
            topics = [topics]
        if type(topics) is list and topics != [] and topics is not None:
            for t in topics:
                if t != "":
                    clscor_mapped = mapping.vocab_mapping_method.get(t)
                    if clscor_mapped is not None:
                        if type(clscor_mapped) is not list:
                            clscor_mapped = [clscor_mapped]
                        for cm in clscor_mapped:
                            result.append(URIRef(cm))
                    else:
                        result.append(CRM_METHOD[t.replace(" ", "_")])
    return result


def _transform_file_type(file_type_data):
    if type(file_type_data) is str:
        file_type_data = [file_type_data]
    result = []
    for ft in file_type_data:
        result.append(CRM_FORMAT[ft.replace(" ", "_")])
    return result


def get_data_veld_uris(veld_data):
    result = _get_veld_uri_by_type(veld_data, "data")
    return result


def get_data_veld_uris__as_chain_input(veld_data):
    result = _get_data_veld_uris__as_chain_io(veld_data, "input")
    return result


def get_data_veld_uris__as_chain_output(veld_data):
    result = _get_data_veld_uris__as_chain_io(veld_data, "output")
    return result


def get_data_veld_label(veld_data):
    result = []
    if _check_if_type(veld_data, "data"):
        result = _get_veld_label(veld_data)
    return result


def get_data_veld_file_type(veld_data):
    result = []
    file_type = _get_data_recursively(veld_data, ["content", "x-veld", "data", "file_type"])
    if file_type is not None:
        result = _transform_file_type(file_type)
    return result


def get_code_veld_label(veld_data):
    result = []
    if _check_if_type(veld_data, "code"):
        result = _get_veld_label(veld_data)
    return result


def get_code_veld_uris(veld_data):
    result = _get_veld_uri_by_type(veld_data, "code")
    return result


def get_code_ved__file_type_inputs(veld_data):
    return _get_code_ved__file_type__of_io(veld_data, "input")


def get_code_ved__file_type_outputs(veld_data):
    return _get_code_ved__file_type__of_io(veld_data, "output")


def get_chain_veld_uris(veld_data):
    result = _get_veld_uri_by_type(veld_data, "chain")
    return result


def get_chain_veld_label(veld_data):
    result = []
    if _check_if_type(veld_data, "chain"):
        result = _get_veld_label(veld_data)
    return result


def get_x5_uri_from_chain(veld_data):
    result = []
    if _get_data_recursively(veld_data, ["content", "x-veld", "chain"]) is not None:
        chain_repo_url = "/".join(veld_data["url"].split("/")[:5])
        result = [URIRef(chain_repo_url)]
    return result


def get_integrated_code_veld_id(veld_data):
    result = []
    if _get_data_recursively(veld_data, ["content", "x-veld", "chain"]) is not None:
        services = _get_data_recursively(veld_data, ["content", "services"])
        if services is not None:
            code_veld_file_list = []
            for s in services.values():
                code_veld_file = _get_data_recursively(s, ["extends", "file"])
                if code_veld_file is not None:
                    code_veld_file_list.append(code_veld_file)
            for code_veld_file in code_veld_file_list:
                code_veld_file = code_veld_file.replace("./code/", "./")
                code_veld_id = code_veld_file[2:].replace("/", "___")
                code_veld_data = VELD_DATA_ALL.get(code_veld_id)
                if code_veld_data is not None:
                    code_veld_uri = get_code_veld_uris(code_veld_data)
                    if code_veld_uri is not None:
                        result.extend(code_veld_uri)
    return result


def get_attribute_assignment_uris(veld_data):
    result = []
    if _get_data_recursively(veld_data, ["content", "x-veld", "data"]) is None:
        hash = _generate_hash(veld_data["url"])
        result = [CLS[hash]]
    return result


def get_cls_tool_description_event_uris(_):
    hash = _generate_hash("random hash for one tool description event")
    uri = CLS[hash]
    return [uri]


def get_code_or_chain_veld_yaml_url(veld_data):
    result_code = _get_veld_uri_by_type(veld_data, "code")
    result_chain = _get_veld_uri_by_type(veld_data, "chain")
    if result_code:
        return result_code
    elif result_chain:
        return result_chain
    else:
        return []


def get_method_uris(veld_data):
    result_code = _get_data_recursively(veld_data, ["content", "x-veld", "code"])
    if result_code:
        result_code = _get_topic(veld_data)
    result_chain = _get_data_recursively(veld_data, ["content", "x-veld", "chain"])
    if result_chain:
        result_chain = _get_topic(veld_data)
    if result_code:
        return result_code
    elif result_chain:
        return result_chain
    else:
        return []


def main():
    g = Graph()
    g.bind("pem", PEM)
    g.bind("crm", CRM)
    g.bind("crmcls", CRMCLS)
    
    for veld_key, veld_data in VELD_DATA_ALL.items():
        print("# VELD: ", veld_key)
        for m_id, m in mapping.mappings.items():
            print("## mapping: ", m_id)
            m_instantiated = {}
            for k, v in m.items():
                if type(v) is types.FunctionType:
                    result = v(veld_data)
                    m_instantiated[k] = result
                else:
                    m_instantiated[k] = [v]
            for s in m_instantiated["s"]:
                for p in m_instantiated["p"]:
                    for o in m_instantiated["o"]:
                        print(f"<{s}> <{p}> <{o}> .")
                        g.add((s, p, o))
        print()
    
    with open(OUT_TTL_DATA_PATH, "w") as f:
        f.write(g.serialize(format="turtle"))
                                    

if __name__ == "__main__":
    main()
