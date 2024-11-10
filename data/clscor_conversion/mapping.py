from src.convert_to_clscor import *


mappings = {
    "data_instances": {
        "s": get_data_veld_instances,
        "p": "<rdf:type>",
        "o": "clscor:data_veld",
    },
    "code_instances": {
        "s": get_code_veld_instances,
        "p": "<rdf:type>",
        "o": "clscor:code_veld",
    },
    "chain_instances": {
        "s": get_chain_veld_instances,
        "p": "<rdf:type>",
        "o": "clscor:chain_veld",
    },
    "chain_instances__code": {
        "s": get_chain_veld_instances,
        "p": "<chain_to_code>",
        "o": get_integrated_code_veld_id,
    },
    "code__code_reification_to_topic": {
        "s": get_code_veld_instances,
        "p": "<code__code_reification_to_topic>",
        "o": get_code_reification_to_topic,
    },
    "code_reification_to_topic__topic": {
        "s": get_code_reification_to_topic,
        "p": "<code_reification_to_topic__topic>",
        "o": get_topic_of_code_reification_to_topic,
    },
    "code__code_to_input_file_type": {
        "s": get_code_veld_instances,
        "p": "<code_takes_input_file_type>",
        "o": get_code_input_file_type,
    },
}
