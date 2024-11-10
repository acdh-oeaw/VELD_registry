from src.convert_to_clscor import *


mappings = {
    "data_uri a PE19": {
        "s": get_data_veld_uris,
        "p": "rdf:type",
        "o": "pem:PE19_Persistent_Digital_Object",
    },
    "code_uri a PE23": {
        "s": get_code_veld_uris,
        "p": "rdf:type",
        "o": "pem:PE23_Volatile_Software",
    },
    "chain_uri a X5": {
        "s": get_chain_veld_uris,
        "p": "rdf:type",
        "o": "crmcls:X5_Research_Activity",
    },
    "chain_uri a PE23": {
        "s": get_chain_veld_uris,
        "p": "rdf:type",
        "o": "pem:PE23_Volatile_Software",
    },
    "chain_uri crmcls:Y7_uses code_uri": {
        "s": get_chain_veld_uris,
        "p": "crmcls:Y7_uses",
        "o": get_integrated_code_veld_id,
    },
    "chain_uri hadInput data_uri": {
        "s": get_chain_veld_uris,
        "p": "<hadInput>",
        "o": get_data_veld_uris__as_chain_input,
    },
    "chain_uri generatedOutput data_uri": {
        "s": get_chain_veld_uris,
        "p": "<generatedOutput>",
        "o": get_data_veld_uris__as_chain_output,
    },
    "chain_uri type X6": {
        "s": get_chain_veld_uris,
        "p": "<type>",
        "o": get_chain_topic_as_x6,
    },
    "code_uri crmcls:Y8_implements X6": {
        "s": get_code_veld_uris,
        "p": "crmcls:Y8_implements",
        "o": get_code_topic_as_x6,
    },
}
