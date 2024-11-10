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
    "chain_uri hadInput data_uri (PE19)": {
        "s": get_chain_veld_uris,
        "p": "<hadInput>",
        "o": get_data_veld_uris__as_chain_input,
    },
    
    "code__to__reification_code_to_topic": {
        "s": get_code_veld_uris,
        "p": "<code__code_reification_to_topic>",
        "o": get_code_reification_to_topic,
    },
    "reification_code_to_topic__to__topic": {
        "s": get_code_reification_to_topic,
        "p": "<code_reification_to_topic__topic>",
        "o": get_topic_of_code_reification_to_topic,
    },
    "code__code_to_input_file_type": {
        "s": get_code_veld_uris,
        "p": "<code_takes_input_file_type>",
        "o": get_code_input_file_type,
    },
}
