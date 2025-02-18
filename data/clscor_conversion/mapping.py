from data.clscor_conversion.rdf_modules_namespaces import *
from src.clscor_convert import *


mappings = {
    
    # data velds
    "data veld Y2 to file type": {
        "s": get_data_veld_uris,
        "p": CRMCLS["Y2_has_format"],
        "o": get_data_veld_file_type,
    },
    "data veld url a PE19": {
        "s": get_data_veld_uris,
        "p": RDF.type,
        "o": PEM["PE19_Persistent_Digital_Object"],
    },
    "data veld url rdfs:label label": {
        "s": get_data_veld_uris,
        "p": RDFS.label,
        "o": get_data_veld_label,
    },
    
    # code velds
    "code veld Y9 X7": {
        "s": get_code_veld_uris,
        "p": CRMCLS["Y9_expects_input"],
        "o": get_code_veld__file_type_inputs,
    },
    "code veld Y10 X7": {
        "s": get_code_veld_uris,
        "p": CRMCLS["Y10_generates_output"],
        "o": get_code_veld__file_type_outputs,
    },
    "code veld url a X12": {
        "s": get_code_veld_uris,
        "p": RDF.type,
        "o": CRMCLS["X12_Tool"],
    },
    "code veld url rdfs:label label": {
        "s": get_code_veld_uris,
        "p": RDFS.label,
        "o": get_code_veld_label,
    },
    
    # chain velds
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
    "chain veld url a X12": {
        "s": get_chain_veld_uris,
        "p": RDF.type,
        "o": CRMCLS["X12_Tool"],
    },
    "chain veld url a PE23": {
        "s": get_chain_veld_uris,
        "p": RDF.type,
        "o": PEM["PE23_Volatile_Software"],
    },
    "chain veld url rdfs:label label": {
        "s": get_chain_veld_uris,
        "p": RDFS.label,
        "o": get_chain_veld_label,
    },
    
    # Attribute Assignments Y8
    "assignment_uri_y8 a E13": {
        "s": get_attribute_assignment_uris_y8,
        "p": RDF.type,
        "o": CRM["E13_Attribute_Assignment"]
    },
    "assignment_uri_y8 P134 tool_description_uri": {
        "s": get_attribute_assignment_uris_y8,
        "p": CRM["P134_continued"],
        "o": get_cls_tool_description_event_uris
    },
    "assignment_uri_y8 P140 code or chain veld url": {
        "s": get_attribute_assignment_uris_y8,
        "p": CRM["P140_assigned_attribute_to"],
        "o": get_code_or_chain_veld_yaml_url,
    },
    "assignment_uri_y8 P141 method uri": {
        "s": get_attribute_assignment_uris_y8,
        "p": CRM["P141_assigned"],
        "o": get_method_uris,
    },
    "assignment_uri_y8 P177 Y8": {
        "s": get_attribute_assignment_uris_y8,
        "p": CRM["P177_assigned_property_of_type"],
        "o": CRMCLS["Y8_implements"],
    },
    
    # Attribute Assignments Y9
    "assignment_uri_y9 a E13": {
        "s": get_attribute_assignment_uris_y9,
        "p": RDF.type,
        "o": CRM["E13_Attribute_Assignment"]
    },
    "assignment_uri_y9 P134 tool_description_uri": {
        "s": get_attribute_assignment_uris_y9,
        "p": CRM["P134_continued"],
        "o": get_cls_tool_description_event_uris
    },
    "assignment_uri_y9 P140 code or chain veld url": {
        "s": get_attribute_assignment_uris_y9,
        "p": CRM["P140_assigned_attribute_to"],
        "o": get_code_or_chain_veld_yaml_url,
    },
    "assignment_uri_y9 P141 method uri": {
        "s": get_attribute_assignment_uris_y9,
        "p": CRM["P141_assigned"],
        "o": get_code_or_chain_veld_input_format,
    },
    "assignment_uri_y9 P177 Y9": {
        "s": get_attribute_assignment_uris_y9,
        "p": CRM["P177_assigned_property_of_type"],
        "o": CRMCLS["Y9_expects_input"],
    },
}


vocab_mapping_method = {
    "NLP": "https://clscor.io/entity/type/method/applying_nlp_methods",
    "Data Cleaning": "https://clscor.io/entity/type/method/information_extraction",
    "Dependency Parsing": "https://clscor.io/entity/type/method/text_parsing",
    "ETL": "https://clscor.io/entity/type/method/information_extraction",
    "Evaluation": "https://clscor.io/entity/type/method/quantitative_analysis",
    "Grammatical Annotation": [
        "https://clscor.io/entity/type/method/annotating",
        "https://clscor.io/entity/type/method/semi_automatical_token_annotation",
        "https://clscor.io/entity/type/method/automatic_annotation",
    ],
    "Lemmatization": "https://clscor.io/entity/type/method/lemmatization",
    "Machine Learning": "https://clscor.io/entity/type/method/machine_learning",
    "Named Entity Recognition": "https://clscor.io/entity/type/method/named_entity_recognition",
    "Part Of Speech": "https://clscor.io/entity/type/method/part_of_speech_tagging",
    "Preprocessing": "https://clscor.io/entity/type/method/information_extraction",
    "Tokenization": "https://clscor.io/entity/type/method/tokenization",
    "Word Embeddings": "https://clscor.io/entity/type/method/word_embedding",
}