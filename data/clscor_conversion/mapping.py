from data.clscor_conversion.rdf_modules_namespaces import *
from src.clscor_convert import *


mappings = {
    "chain repo url a X5": {
        "s": get_x5_uri_from_chain,
        "p": RDF.type,
        "o": CRMCLS["X5_Research_Activity"],
    },
    "X5 to chain": {
        "s": get_x5_uri_from_chain,
        "p": CRMCLS["Y7_uses"],
        "o": get_chain_veld_uris,
    },
    "X5 had input PE19 (data veld)": {
        "s": get_x5_uri_from_chain,
        "p": CRMCLS["hadInput"],
        "o": get_data_veld_uris__as_chain_input,
    },
    "X5 generated output PE19 (data veld)": {
        "s": get_x5_uri_from_chain,
        "p": CRMCLS["generatedOutput"],
        "o": get_data_veld_uris__as_chain_output,
    },
    "chain Y7 code": {
        "s": get_chain_veld_uris,
        "p": CRMCLS["Y7_uses"],
        "o": get_integrated_code_veld_id,
    },
    "data veld Y2 to file type": {
        "s": get_data_veld_uris,
        "p": CRMCLS["Y2_has_format"],
        "o": get_data_veld_file_type,
    },
    "code veld Y9 X7": {
        "s": get_code_veld_uris,
        "p": CRMCLS["Y9_expects_input"],
        "o": get_code_ved__file_type_inputs,
    },
    "code veld Y10 X7": {
        "s": get_code_veld_uris,
        "p": CRMCLS["Y10_generates_output"],
        "o": get_code_ved__file_type_outputs,
    },
    "data_uri a PE19": {
        "s": get_data_veld_uris,
        "p": RDF.type,
        "o": PEM["PE19_Persistent_Digital_Object"],
    },
    "code_uri a X12": {
        "s": get_code_veld_uris,
        "p": RDF.type,
        "o": CRMCLS["X12_Tool"],
    },
    "chain_uri a X12": {
        "s": get_chain_veld_uris,
        "p": RDF.type,
        "o": CRMCLS["X12_Tool"],
    },
    "chain_uri a PE23": {
        "s": get_chain_veld_uris,
        "p": RDF.type,
        "o": PEM["PE23_Volatile_Software"],
    },
    "code_uri crmcls:Y8_implements X6": {
        "s": get_code_veld_uris,
        "p": CRMCLS["Y8_implements"],
        "o": get_code_topic_as_x6,
    },
}
