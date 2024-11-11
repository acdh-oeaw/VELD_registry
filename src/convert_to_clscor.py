import types

import yaml
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS


IN_VELD_DATA_PATH = "/app/data/veld_files/merged/all_velds_merged.yaml"
with open(IN_VELD_DATA_PATH, "r") as f:
    VELD_DATA_ALL = yaml.safe_load(f)
OUT_TTL_DATA_PATH = "/app/data/clscor_conversion/output.ttl"
    
CRMCLS = Namespace("https://clscor.io/ontologies/CRMcls/")

    
def _get_veld_uri_by_type(veld_data, veld_type):
    result = []
    try:
        _ = veld_data["content"]["x-veld"][veld_type]
        _ = veld_data["url"]
    except KeyError:
        pass
    else:
        result = [URIRef(veld_data["url"])]
    return result


def get_data_veld_uris(veld_data):
    result = _get_veld_uri_by_type(veld_data, "data")
    return result


def _get_data_veld_uris__as_chain_input_or_output(veld_data, direction):
    result = []
    try:
        _ = veld_data["content"]["x-veld"]["chain"]
        services = veld_data["content"]["services"]
        volumes_list = []
        for s in services.values():
            for vol in s.get("volumes"):
                volumes_list.append(vol)
    except:
        pass
    else:
        data_veld_uris = {}
        for data_veld_id, data_veld_data in VELD_DATA_ALL.items():
            try:
                _ = data_veld_data["content"]["x-veld"]["data"]
            except:
                pass
            else:
                data_veld_uris[data_veld_id] = data_veld_data["url"]
        for vol in volumes_list:
            vol = vol.split(":")
            if direction in vol[1]:
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


def get_data_veld_uris__as_chain_input(veld_data):
    result = _get_data_veld_uris__as_chain_input_or_output(veld_data, "input")
    return result


def get_data_veld_uris__as_chain_output(veld_data):
    result = _get_data_veld_uris__as_chain_input_or_output(veld_data, "output")
    return result


def get_code_veld_uris(veld_data):
    result = _get_veld_uri_by_type(veld_data, "code")
    return result


def get_chain_veld_uris(veld_data):
    result = _get_veld_uri_by_type(veld_data, "chain")
    return result


def _get_topic(veld_data):
    result = []
    try:
        topics = list(veld_data["content"]["x-veld"].values())[0]["topics"]
    except:
        pass
    else:
        if type(topics) is str:
            topics = [topics]
        if type(topics) is list and topics != [] and topics is not None:
            for t in topics:
                if t != "":
                    result.append(CRMCLS["X6_METHOD/" + t.replace(" ", "_")])
    return result


def get_code_reification_to_topic(veld_data):
    result = []
    i = 1 # TODO: solve problem with global index
    try:
        _ = veld_data["content"]["x-veld"]["code"]
        topics = veld_data["content"]["x-veld"]["code"]["topics"]
    except:
        pass
    else:
        if topics != "" and topics != [] and topics is not None:
            result = [f"clscor:/code_reification_to_topic_{i}"]
            i += 1
    return result


def get_topic_of_code_reification_to_topic(veld_data):
    result = []
    try:
        _ = veld_data["content"]["x-veld"]["code"]
    except:
        pass
    else:
        result = _get_topic(veld_data)
    return result


def get_code_input_file_type(veld_data):
    result = []
    try:
        _ = veld_data["content"]["x-veld"]["code"]
        input_group_list = veld_data["content"]["x-veld"]["code"]["inputs"]
    except:
        pass
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
            result = inputs
    return result


def get_integrated_code_veld_id(veld_data):
    result = []
    try:
        _ = veld_data["content"]["x-veld"]["chain"]
        services = veld_data["content"]["services"]
        code_veld_file_list = [s["extends"]["file"] for s in services.values()]
    except:
        pass
    else:
        for code_veld_file in code_veld_file_list:
            code_veld_id = code_veld_file[2:].replace("/", "___")
            code_veld_data = VELD_DATA_ALL.get(code_veld_id)
            if code_veld_data is not None:
                code_veld_uri = get_code_veld_uris(code_veld_data)
                if code_veld_uri is not None:
                    result.extend(code_veld_uri)
    return result


def get_chain_topic_as_x6(veld_data):
    result = {}
    try:
        _ = veld_data["content"]["x-veld"]["chain"]
    except:
        pass
    else:
        result = _get_topic(veld_data)
    return result


def get_code_topic_as_x6(veld_data):
    result = []
    try:
        _ = veld_data["content"]["x-veld"]["code"]
    except:
        pass
    else:
        result = _get_topic(veld_data)
    return result


def main():
    from data.clscor_conversion.mapping import mappings, CRMCLS, PEM
    
    g = Graph()
    g.bind("crmcls", CRMCLS)
    g.bind("pem", PEM)
    
    for veld_key, veld_data in VELD_DATA_ALL.items():
        print("# VELD: ", veld_key)
        for m_id, m in mappings.items():
            print("## mapping: ", m_id)
            m_instantiated = {}
            for k, v in m.items():
                if type(v) is types.FunctionType:
                    m_instantiated[k] = v(veld_data)
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
