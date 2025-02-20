import hashlib
import types
import uuid

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


def _is_data_veld(veld_data):
    return _get_data_recursively(veld_data, ["content", "x-veld", "data"]) is not None


def _is_code_veld(veld_data):
    return _get_data_recursively(veld_data, ["content", "x-veld", "code"]) is not None


def _is_chain_veld(veld_data):
    return _get_data_recursively(veld_data, ["content", "x-veld", "chain"]) is not None
    

# TODO: result of this seems a little bit low; check it
def _get_data_veld_uris__as_chain_io_by_io_and_veld(veld_data, io):
    result = []
    volumes_list = []
    if _is_chain_veld(veld_data):
        services = _get_data_recursively(veld_data, ["content", "services"])
        for s in services.values():
            v = s.get("volumes")
            if v is not None:
                for vol in v:
                    volumes_list.append(vol)
    if volumes_list:
        data_veld_uris = {}
        for data_veld_id, data_veld_data in VELD_DATA_ALL.items():
            if _is_data_veld(data_veld_data):
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
                            result.append(CLS[_generate_hash(data_uri + "__uri_hash")])
    return result


def _get_code_veld_file_type_to_format_of_io(veld_data, io_direction):
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


def _get_topic_as_method_uri(veld_data):
    result = []
    veld_data_any = _get_data_recursively(veld_data, ["content", "x-veld"])
    if veld_data_any is not None:
        veld_data_any = list(veld_data_any.values())[0]
        if veld_data_any:
            topics = veld_data_any.get("topic")
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
    result = []
    if type(file_type_data) is str:
        file_type_data = [file_type_data]
    for ft in file_type_data:
        result.append(CRM_FORMAT[ft.replace(" ", "_")])
    return result


def _get_veld_url_by_type(veld_data, veld_type):
    if _get_data_recursively(veld_data, ["content", "x-veld", veld_type]):
        return URIRef(veld_data["url"])
    else:
        return None
    
    
def _get_veld_label(veld_data):
    result = None
    veld_url = veld_data.get("url")
    if veld_url is not None:
        url_part_list = veld_url.split("https://github.com/veldhub/")[1].split("/")
        label_repo = url_part_list[0]
        label_veld = url_part_list[-1].split(".yaml")[0]
        if label_veld == "veld":
            label = label_repo
        else:
            label = label_repo + "__" + label_veld.replace("veld_", "")
        result = Literal(label)
    return result


def _get_veld_label_by_type(veld_data, veld_type):
    result = None
    if _get_data_recursively(veld_data, ["content", "x-veld", veld_type]):
        result = _get_veld_label(veld_data)
    return result


def _get_data_veld_uris__as_chain_io_by_io(io):
    result = {}
    for veld_key, veld_data in VELD_DATA_ALL.items():
        io_result = _get_data_veld_uris__as_chain_io_by_io_and_veld(veld_data, io)
        if io_result:
            result[veld_key] = io_result
    return result
    
    
def get_data_veld_uris():
    result = {}
    for veld_key, veld_data in VELD_DATA_ALL.items():
        veld_uri = _get_veld_url_by_type(veld_data, "data")
        if veld_uri:
            result[veld_key] = [CLS[_generate_hash(veld_uri + "__uri_hash")]]
    return result


def get_code_veld_uris():
    result = {}
    for veld_key, veld_data in VELD_DATA_ALL.items():
        veld_uri = _get_veld_url_by_type(veld_data, "code")
        if veld_uri:
            result[veld_key] = [CLS[_generate_hash(veld_uri + "__uri_hash")]]
    return result


def get_chain_veld_uris():
    result = {}
    for veld_key, veld_data in VELD_DATA_ALL.items():
        veld_uri = _get_veld_url_by_type(veld_data, "chain")
        if veld_uri:
            result[veld_key] = [CLS[_generate_hash(veld_uri + "__uri_hash")]]
    return result


def get_chain_or_code_veld_uris():
    result = {}
    for veld_key, veld_data in VELD_DATA_ALL.items():
        veld_uri = None
        code_uri = _get_veld_url_by_type(veld_data, "code")
        chain_uri = _get_veld_url_by_type(veld_data, "chain")
        if code_uri:
            veld_uri = code_uri
        if chain_uri:
            veld_uri = chain_uri
        if veld_uri:
            result[veld_key] = [CLS[_generate_hash(veld_uri + "__uri_hash")]]
    return result


def get_all_veld_uris():
    result = {}
    for veld_key, veld_data in VELD_DATA_ALL.items():
        veld_uri = URIRef(veld_data["url"])
        result[veld_key] = [CLS[_generate_hash(veld_uri + "__uri_hash")]]
    return result
    
    
def get_data_veld_file_type():
    result = {}
    for veld_key, veld_data in VELD_DATA_ALL.items():
        file_type = _get_data_recursively(veld_data, ["content", "x-veld", "data", "file_type"])
        if file_type:
            result[veld_key] = _transform_file_type(file_type)
    return result


def get_data_veld_label():
    result = {}
    for veld_key, veld_data in VELD_DATA_ALL.items():
        veld_label = _get_veld_label_by_type(veld_data, "data")
        if veld_label:
            result[veld_key] = [veld_label]
    return result


def get_code_veld_label():
    result = {}
    for veld_key, veld_data in VELD_DATA_ALL.items():
        veld_label = _get_veld_label_by_type(veld_data, "code")
        if veld_label:
            result[veld_key] = [veld_label]
    return result


def get_data_veld_uris__as_chain_input():
    return _get_data_veld_uris__as_chain_io_by_io("input")


def get_data_veld_uris__as_chain_output():
    return _get_data_veld_uris__as_chain_io_by_io("output")


def get_integrated_code_veld_uri():
    result = {}
    for veld_key, veld_data in VELD_DATA_ALL.items():
        if _is_chain_veld(veld_data):
            services = _get_data_recursively(veld_data, ["content", "services"])
            if services is not None:
                code_veld_file_list = []
                for s in services.values():
                    code_veld_file = _get_data_recursively(s, ["extends", "file"])
                    if code_veld_file is not None:
                        code_veld_file_list.append(code_veld_file)
                result_per_veld_key = []
                for code_veld_file in code_veld_file_list:
                    code_veld_file = code_veld_file.replace("./code/", "./")
                    code_veld_id = code_veld_file[2:].replace("/", "___")
                    code_veld_data = VELD_DATA_ALL.get(code_veld_id)
                    if code_veld_data is not None:
                        code_veld_uri = _get_veld_url_by_type(code_veld_data, "code")
                        if code_veld_uri is not None:
                            result_per_veld_key.append(CLS[_generate_hash(code_veld_uri + "__uri_hash")])
                if result_per_veld_key:
                    result[veld_key] = result_per_veld_key
    return result


def get_x5_uri_from_chain():
    result = {}
    for veld_key, veld_data in VELD_DATA_ALL.items():
        if _is_chain_veld(veld_data):
            chain_repo_url = "/".join(veld_data["url"].split("/")[:5])
            result[veld_key] = [URIRef(chain_repo_url)]
    return result


def get_chain_veld_label():
    result = {}
    for veld_key, veld_data in VELD_DATA_ALL.items():
        veld_label = _get_veld_label_by_type(veld_data, "chain")
        if veld_label:
            result[veld_key] = [veld_label]
    return result


def get_chain_or_code_veld_label():
    result = {}
    for veld_key, veld_data in VELD_DATA_ALL.items():
        veld_label = None
        code_label = _get_veld_label_by_type(veld_data, "code")
        chain_label = _get_veld_label_by_type(veld_data, "chain")
        if code_label:
            veld_label = code_label
        if chain_label:
            veld_label = chain_label
        if veld_label:
            result[veld_key] = [veld_label]
    return result


def get_chain_or_code_veld_appellation_and_id():
    result = {}
    for veld_key, veld_data in VELD_DATA_ALL.items():
        veld_uri = None
        code_uri = _get_veld_url_by_type(veld_data, "code")
        chain_uri = _get_veld_url_by_type(veld_data, "chain")
        if code_uri:
            veld_uri = code_uri
        if chain_uri:
            veld_uri = chain_uri
        if veld_uri:
            veld_uuid = uuid.uuid5(uuid.uuid5(uuid.NAMESPACE_DNS, CLS), veld_key + "__appellation_id")
            result[veld_key] = [CLS[str(veld_uuid)]]
    return result


def get_all_veld_appellation_uri():
    result = {}
    for veld_key, veld_data in VELD_DATA_ALL.items():
        veld_uuid = uuid.uuid5(uuid.uuid5(uuid.NAMESPACE_DNS, CLS), veld_key + "__appellation_id")
        result[veld_key] = [CLS[str(veld_uuid)]]
    return result


def get_all_veld_appellation_type():
    result = {}
    for veld_key, veld_data in VELD_DATA_ALL.items():
        if _is_data_veld(veld_data):
            result[veld_key] = [CLS_APLTN["data_veld"]]
        if _is_code_veld(veld_data):
            result[veld_key] = [CLS_APLTN["code_veld"]]
        if _is_chain_veld(veld_data):
            result[veld_key] = [CLS_APLTN["chain_veld"]]
    return result


def get_all_veld_appellation_label():
    result = {}
    for veld_key, veld_data in VELD_DATA_ALL.items():
        label = _get_veld_label(veld_data)
        result[veld_key] = [label]
    return result


def get_all_veld_identifier_uri():
    result = {}
    for veld_key, veld_data in VELD_DATA_ALL.items():
        veld_uuid = uuid.uuid5(uuid.uuid5(uuid.NAMESPACE_DNS, CLS), veld_key)
        result[veld_key] = [CLS[str(veld_uuid)]]
    return result
    
    
def get_attribute_assignment_uris_y8():
    result = {}
    for veld_key, veld_data in VELD_DATA_ALL.items():
        if (
            _is_code_veld(veld_data)
            or _is_chain_veld(veld_data)
        ):
            methods = _get_topic_as_method_uri(veld_data)
            for i, m in enumerate(methods):
                hashed_uri = _generate_hash(veld_data["url"] + "_y8" + m)
                result[veld_key + "__" + str(i)] = [CLS[hashed_uri]]
    return result


def get_cls_tool_description_event_uris_y8():
    result = {}
    for veld_key, veld_data in VELD_DATA_ALL.items():
        if (
            _is_code_veld(veld_data)
            or _is_chain_veld(veld_data)
        ):
            methods = _get_topic_as_method_uri(veld_data)
            hashed_uri = _generate_hash(veld_data["url"] + "description_event")
            for i, m in enumerate(methods):
                result[veld_key + "__" + str(i)] = [CLS[hashed_uri]]
    return result


def get_method_uris():
    result = {}
    for veld_key, veld_data in VELD_DATA_ALL.items():
        if (
            _is_code_veld(veld_data)
            or _is_chain_veld(veld_data)
        ):
            methods_uri = _get_topic_as_method_uri(veld_data)
            for i, m in enumerate(methods_uri):
                result[veld_key + "__" + str(i)] = [m]
    return result


def get_code_or_chain_veld_uri_per_method():
    result = {}
    for veld_key, veld_data in VELD_DATA_ALL.items():
        veld_uri = None
        code_veld_uri = _get_veld_url_by_type(veld_data, "code")
        chain_veld_uri = _get_veld_url_by_type(veld_data, "chain")
        if code_veld_uri:
            veld_uri = code_veld_uri
        if chain_veld_uri:
            veld_uri = chain_veld_uri
        if veld_uri:
            methods = _get_topic_as_method_uri(veld_data)
            for i, m in enumerate(methods):
                result[veld_key + "__" + str(i)] = [CLS[_generate_hash(veld_uri + "__uri_hash")]]
    return result


def get_attribute_assignment_uris_regarding_y9_or_y10_by_io(io):
    result = {}
    for veld_key, veld_data in VELD_DATA_ALL.items():
        if (
            _is_code_veld(veld_data)
             and _get_code_veld_file_type_to_format_of_io(veld_data, io)
        ):
            hashed_uri = _generate_hash(veld_key + "attribute_assignment__y9_and_y10__" + io)
            result[veld_key] = [CLS[hashed_uri]]
    return result


def get_attribute_assignment_uris_regarding_y9_input():
    return get_attribute_assignment_uris_regarding_y9_or_y10_by_io("input")


def get_attribute_assignment_uris_regarding_y10_output():
    return get_attribute_assignment_uris_regarding_y9_or_y10_by_io("output")
    
    
def get_tool_description_event_uris_y9_and_y10():
    result = {}
    for veld_key, veld_data in VELD_DATA_ALL.items():
        if (
            _is_code_veld(veld_data)
             and (
                _get_code_veld_file_type_to_format_of_io(veld_data, "input")
                or _get_code_veld_file_type_to_format_of_io(veld_data, "output")
            )
        ):
            hashed_uri = _generate_hash(veld_key + "tool_description_event__y9_and_y10")
            result[veld_key] = [CLS[hashed_uri]]
    return result
    
    
def get_code_veld_input_or_output_format(io):
    result = {}
    for veld_key, veld_data in VELD_DATA_ALL.items():
        if _is_code_veld(veld_data):
            io_result = _get_code_veld_file_type_to_format_of_io(veld_data, io)
            if io_result:
                result[veld_key] = io_result
    return result
    
    
def get_code_veld_input_format():
    return get_code_veld_input_or_output_format("input")


def get_code_veld_output_format():
    return get_code_veld_input_or_output_format("output")
    


def main():
    
    def check(a, b):
        return "_" in [a, b] or a == b
    
    g = Graph()
    g.bind("pem", PEM)
    g.bind("crm", CRM)
    g.bind("crmcls", CRMCLS)
    
    for m_id, m in mapping.mappings.items():
        print("## mapping: ", m_id)
        m_instantiated = {}
        for k, v in m.items():
            if type(v) is types.FunctionType:
                print("executing:", v.__name__)
                result = v()
                m_instantiated[k] = result
            else:
                m_instantiated[k] = {"_": [v]}
        for s_k, s_v in m_instantiated["s"].items():
            for p_k, p_v in m_instantiated["p"].items():
                for o_k, o_v in m_instantiated["o"].items():
                    if check(s_k, p_k) and check(s_k, o_k) and check(p_k, o_k):
                        for s in s_v:
                            for p in p_v:
                                for o in o_v:
                                    print(f"<{s}> <{p}> <{o}> .")
                                    g.add((s, p, o))
                                    
    with open(OUT_TTL_DATA_PATH, "w") as f:
        f.write(g.serialize(format="turtle"))
                                    

if __name__ == "__main__":
    main()
