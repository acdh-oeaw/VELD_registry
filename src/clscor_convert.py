import hashlib
import types
import uuid

import yaml

from data.clscor_conversion.rdf_modules_namespaces import *
from data.clscor_conversion import mapping


IN_VELD_DATA_PATH = "/app/data/veld_files/merged/all_velds_merged.yaml"
# IN_VELD_DATA_PATH = "/app/data/veld_files/merged/all_velds_merged_sample.yaml"
with open(IN_VELD_DATA_PATH, "r") as f:
    VELD_DATA_ALL = yaml.safe_load(f)
OUT_TTL_DATA_PATH = "/app/data/clscor_conversion/output.ttl"
# OUT_TTL_DATA_PATH = "/app/data/clscor_conversion/output_sample.ttl"


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
        data_veld_path_url_dict = {}
        for data_veld_id, data_veld_data in VELD_DATA_ALL.items():
            if _is_data_veld(data_veld_data):
                data_veld_name = data_veld_id.split("___")[0]
                data_veld_path_url_dict[data_veld_name] = data_veld_data["url"]
        for vol in volumes_list:
            vol = vol.split(":")
            if io in vol[1]:
                chain_data_path = vol[0][2:]
                chain_data_path = chain_data_path.split("/")
                for chain_data_path_part in chain_data_path:
                    data_veld_url = data_veld_path_url_dict.get(chain_data_path_part)
                    if data_veld_url:
                        result.append(CLS[_generate_hash(data_veld_url)])
                        print(data_veld_url)
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


def _get_topic_as_method_uri(veld_data):
    result = set()
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
                                result.add(URIRef(cm))
                        else:
                            result.add(CLS_METHOD[t.replace(" ", "_")])
    result = sorted(list(result))
    return result


def _transform_file_type(file_type_data):
    result = []
    if type(file_type_data) is str:
        file_type_data = [file_type_data]
    for ft in file_type_data:
        result.append(CLS_FORMAT[ft.replace(" ", "_")])
    return result


def _get_veld_url_by_type(veld_data, veld_type):
    if _get_data_recursively(veld_data, ["content", "x-veld", veld_type]):
        return URIRef(veld_data["url"])
    else:
        return None
    
    
def _get_veld_label(veld_data):
    url_part_list = veld_data["url"].split("https://github.com/veldhub/")[1].split("/")
    label = url_part_list[0]
    suffix = ""
    if label.startswith("veld_data"):
        suffix = " (data veld)"
        label = label.replace("veld_data", "")
    elif label.startswith("veld_code"):
        suffix = " (code veld)"
        label = label.replace("veld_code", "")
    elif label.startswith("veld_chain"):
        suffix = " (chain veld)"
        label = label.replace("veld_chain", "")
    label = label.replace("__", "")
    label_veld = url_part_list[-1].split(".yaml")[0]
    if label_veld.startswith("veld_"):
        label += ": " + label_veld.replace("veld_", "")
    label = label.replace("_", " ")
    label += suffix
    result = Literal(label)
    return result


def _get_data_veld_uris__as_chain_io_by_io(io):
    result = {}
    for veld_key, veld_data in VELD_DATA_ALL.items():
        io_result = _get_data_veld_uris__as_chain_io_by_io_and_veld(veld_data, io)
        if io_result:
            result[veld_key] = io_result
    return result


def _get_code_veld_from_chain(veld_data):
    result = {}
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
            result[code_veld_id] = VELD_DATA_ALL.get(code_veld_id)
    return result

    
    
def get_data_veld_uris():
    result = {}
    for veld_key, veld_data in VELD_DATA_ALL.items():
        if _is_data_veld(veld_data):
            result[veld_key] = [CLS[_generate_hash(veld_data["url"])]]
    return result


def get_code_veld_uris():
    result = {}
    for veld_key, veld_data in VELD_DATA_ALL.items():
        if _is_code_veld(veld_data):
            result[veld_key] = [CLS[_generate_hash(veld_data["url"])]]
    return result


def get_chain_veld_uris():
    result = {}
    for veld_key, veld_data in VELD_DATA_ALL.items():
        if _is_chain_veld(veld_data):
            result[veld_key] = [CLS[_generate_hash(veld_data["url"])]]
    return result


def get_all_veld_uris():
    result = {}
    for veld_key, veld_data in VELD_DATA_ALL.items():
        result[veld_key] = [CLS[_generate_hash(veld_data["url"])]]
    return result


def get_all_veld_urls():
    result = {}
    for veld_key, veld_data in VELD_DATA_ALL.items():
        result[veld_key] = [URIRef(veld_data["url"])]
    return result


def get_data_description():
    result = {}
    for veld_key, veld_data in VELD_DATA_ALL.items():
        veld_data_data = _get_data_recursively(veld_data, ["content", "x-veld"])
        veld_data_data_data = list(veld_data_data.values())[0]
        desc = _get_data_recursively(veld_data_data_data, ["description"])
        if desc:
            result[veld_key] = [Literal(desc)]
    return result
    
    
def get_data_veld_file_type():
    result = {}
    for veld_key, veld_data in VELD_DATA_ALL.items():
        file_type = _get_data_recursively(veld_data, ["content", "x-veld", "data", "file_type"])
        if file_type:
            result[veld_key] = _transform_file_type(file_type)
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
                        if _is_code_veld(code_veld_data):
                            result_per_veld_key.append(CLS[_generate_hash(code_veld_data["url"])])
                if result_per_veld_key:
                    result[veld_key] = result_per_veld_key
    return result


def get_x5_uri_from_chain():
    result = {}
    for veld_key, veld_data in VELD_DATA_ALL.items():
        if _is_chain_veld(veld_data):
            chain_repo_url = "/".join(veld_data["url"].split("/")[:5])
            result[veld_key] = [CLS[_generate_hash(chain_repo_url)]]
    return result


def get_all_veld_appellation_uri():
    result = {}
    for veld_key, veld_data in VELD_DATA_ALL.items():
        veld_uuid = uuid.uuid5(uuid.uuid5(uuid.NAMESPACE_DNS, CLS), veld_key + "__e41")
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


def get_all_veld_e42_uri():
    result = {}
    for veld_key, veld_data in VELD_DATA_ALL.items():
        veld_uuid = uuid.uuid5(uuid.uuid5(uuid.NAMESPACE_DNS, CLS), veld_key + "__e42")
        result[veld_key] = [CLS[str(veld_uuid)]]
    return result
    
    
def get_x13_per_code_or_chain_veld():
    result = {}
    for veld_key, veld_data in VELD_DATA_ALL.items():
        if _is_code_veld(veld_data) or _is_chain_veld(veld_data):
            hashed_uri = _generate_hash(veld_data["url"] + "__x13")
            result[veld_key] = [CLS[hashed_uri]]
    return result


def get_e13_per_veld_per_y8():
    result = {}
    for veld_key, veld_data in VELD_DATA_ALL.items():
        if _is_code_veld(veld_data) or _is_chain_veld(veld_data):
            methods = _get_topic_as_method_uri(veld_data)
            for i in range(len(methods)):
                hashed_uri = _generate_hash(veld_key + "__e13__y8__" + str(i))
                result[veld_key + "__e13__y8__" + str(i)] = [CLS[hashed_uri]]
    return result


def get_veld_uri_per_e13_per_y8():
    result = {}
    for veld_key, veld_data in VELD_DATA_ALL.items():
        if _is_code_veld(veld_data) or _is_chain_veld(veld_data):
            methods = _get_topic_as_method_uri(veld_data)
            result_tmp = []
            for i in range(len(methods)):
                hashed_uri = _generate_hash(veld_data["url"])
                result_tmp.append(CLS[hashed_uri])
                result[veld_key + "__e13__y8__" + str(i)] = result_tmp
    return result


def get_x13_per_e13_per_y8():
    result = {}
    for veld_key, veld_data in VELD_DATA_ALL.items():
        if _is_code_veld(veld_data) or _is_chain_veld(veld_data):
            methods = _get_topic_as_method_uri(veld_data)
            result_tmp = []
            for i in range(len(methods)):
                hashed_uri = _generate_hash(veld_data["url"] + "__x13")
                result_tmp.append(CLS[hashed_uri])
                result[veld_key + "__e13__y8__" + str(i)] = result_tmp
    return result


def get_method_per_e13_per_y8():
    result = {}
    for veld_key, veld_data in VELD_DATA_ALL.items():
        if _is_code_veld(veld_data) or _is_chain_veld(veld_data):
            methods = _get_topic_as_method_uri(veld_data)
            for i, m in enumerate(methods):
                result[veld_key + "__e13__y8__" + str(i)] = [m]
    return result


def _get_io_of_code_or_chain(veld_data, io):
    result = []
    if _is_code_veld(veld_data):
        result = _get_code_veld_file_type_to_format_of_io(veld_data, io)
    if _is_chain_veld(veld_data):
        code_veld_data_dict = _get_code_veld_from_chain(veld_data)
        for code_veld_data_io in code_veld_data_dict.values():
            result.extend(_get_code_veld_file_type_to_format_of_io(code_veld_data_io, io))
    return result


def _get_y9_or_y10_per_io(io):
    io_id = None
    if io == "input":
        io_id = "y9"
    elif io == "output":
        io_id = "y10"
    return io_id


def _get_e13_per_veld_per_y9_or_y10(io):
    result = {}
    io_id = _get_y9_or_y10_per_io(io)
    for veld_key, veld_data in VELD_DATA_ALL.items():
        io_result = _get_io_of_code_or_chain(veld_data, io)
        for i in range(len(io_result)):
            hashed_uri = _generate_hash(veld_key + "__e13__" + io_id + "__" + str(i))
            result[veld_key + "__e13__" + io_id + "__" + str(i)] = [CLS[hashed_uri]]
    return result


def get_e13_per_veld_per_y9():
    return _get_e13_per_veld_per_y9_or_y10("input")


def get_e13_per_veld_per_y10():
    return _get_e13_per_veld_per_y9_or_y10("output")


def _get_veld_uri_per_e13_per_y9_or_y10(io):
    result = {}
    io_id = _get_y9_or_y10_per_io(io)
    for veld_key, veld_data in VELD_DATA_ALL.items():
        result_tmp = []
        io_result = _get_io_of_code_or_chain(veld_data, io)
        for i in range(len(io_result)):
            hashed_uri = _generate_hash(veld_data["url"])
            result_tmp.append(CLS[hashed_uri])
            result[veld_key + "__e13__" + io_id + "__" + str(i)] = result_tmp
    return result


def get_veld_uri_per_e13_per_y9():
    return _get_veld_uri_per_e13_per_y9_or_y10("input")


def get_veld_uri_per_e13_per_y10():
    return _get_veld_uri_per_e13_per_y9_or_y10("output")


def _get_x13_per_e13_per_y9_or_y10(io):
    result = {}
    io_id = _get_y9_or_y10_per_io(io)
    for veld_key, veld_data in VELD_DATA_ALL.items():
        result_tmp = []
        io_result = _get_io_of_code_or_chain(veld_data, io)
        for i in range(len(io_result)):
            hashed_uri = _generate_hash(veld_data["url"] + "__x13")
            result_tmp.append(CLS[hashed_uri])
            result[veld_key + "__e13__" + io_id + "__" + str(i)] = result_tmp
    return result


def get_x13_per_e13_per_y9():
    return _get_x13_per_e13_per_y9_or_y10("input")


def get_x13_per_e13_per_y10():
    return _get_x13_per_e13_per_y9_or_y10("output")


def _get_format_per_e13_per_y9_or_y10(io):
    result = {}
    io_id = _get_y9_or_y10_per_io(io)
    for veld_key, veld_data in VELD_DATA_ALL.items():
        io_result = _get_io_of_code_or_chain(veld_data, io)
        for i, io_individual in enumerate(io_result):
            result[veld_key + "__e13__" + io_id + "__" + str(i)] = [io_individual]
    return result


def get_format_per_e13_per_y9():
    return _get_format_per_e13_per_y9_or_y10("input")


def get_format_per_e13_per_y10():
    return _get_format_per_e13_per_y9_or_y10("output")
    

def get_pc3_uri():
    result = {}
    for veld_key, veld_data in VELD_DATA_ALL.items():
        veld_data_tmp = _get_data_recursively(veld_data, ["content", "x-veld"])
        veld_data_tmp = list(veld_data_tmp.values())[0]
        if veld_data_tmp:
            description = veld_data_tmp.get("description")
            if description:
                result[veld_key] = [CLS[_generate_hash(veld_data["url"] + "__pc3")]]
    return result


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
