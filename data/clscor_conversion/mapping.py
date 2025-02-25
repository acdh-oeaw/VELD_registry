from data.clscor_conversion.rdf_modules_namespaces import *
from src.clscor_convert import *


mappings = {

    # all velds
    "pc3_instance -a-> PC3": {
        "s": get_pc3_uri,
        "p": RDF.type,
        "o": CRM["PC3_has_note"],
    },
    "pc3_instance -p01-> veld_instance": {
        "s": get_pc3_uri,
        "p": CRM["P01_has_domain"],
        "o": get_all_veld_uris,
    },
    "pc3_instance -p03-> description literal": {
        "s": get_pc3_uri,
        "p": CRM["P03_has_range_literal"],
        "o": get_data_description,
    },
    "pc3_instance -p3.1-> tool_description": {
        "s": get_pc3_uri,
        "p": CRM["P3.1_has_type"],
        "o": CRMCLS["tool_description"],
    },

    # data velds
    "data_veld_instance -a-> PE19": {
        "s": get_data_veld_uris,
        "p": RDF.type,
        "o": PEM["PE19_Persistent_Digital_Object"],
    },
    "data_veld_instance -Y2-> format": {
        "s": get_data_veld_uris,
        "p": CRMCLS["Y2_has_format"],
        "o": get_data_veld_file_type,
    },

    # chain velds
    "chain_veld_instance -a-> PE23": {
        "s": get_chain_veld_uris,
        "p": RDF.type,
        "o": PEM["PE23_Volatile_Software"],
    },
    "X5_instance -a-> X5": {
        "s": get_x5_uri_from_chain,
        "p": RDF.type,
        "o": CRMCLS["X5_Research_Activity"],
    },
    "X5_instance -Y7-> chain_veld_instance": {
        "s": get_x5_uri_from_chain,
        "p": CRMCLS["Y7_uses"],
        "o": get_chain_veld_uris,
    },
    "X5_instance -Y11-> data_veld_instance": {
        "s": get_x5_uri_from_chain,
        "p": CRMCLS["Y11_received_input"],
        "o": get_data_veld_uris__as_chain_input,
    },
    "X5_instance -Y12-> data_veld_instance": {
        "s": get_x5_uri_from_chain,
        "p": CRMCLS["Y12_created_output"],
        "o": get_data_veld_uris__as_chain_output,
    },
    "chain_veld_instance -Y7-> code_veld_instance": {
        "s": get_chain_veld_uris,
        "p": CRMCLS["Y7_uses"],
        "o": get_integrated_code_veld_uri,
    },

    # code and chain velds
    "code_veld_instance -a-> X12": {
        "s": get_chain_veld_uris,
        "p": RDF.type,
        "o": CRMCLS["X12_Tool"],
    },
    "chain_veld_instance -a-> X12": {
        "s": get_code_veld_uris,
        "p": RDF.type,
        "o": CRMCLS["X12_Tool"],
    },

    # veld identification
    "veld_instance -P1-> E41_instance": {
        "s": get_all_veld_uris,
        "p": CRM["P1_is_identified_by"],
        "o": get_all_veld_appellation_uri,
    },
    "E41_instance -a-> E41": {
        "s": get_all_veld_appellation_uri,
        "p": RDF.type,
        "o": CRM["E41_Appellation"],
    },
    "E41_instance -P2-> appellation_type": {
        "s": get_all_veld_appellation_uri,
        "p": CRM["P2_has_type"],
        "o": get_all_veld_appellation_type,
    },
    "E41_instance -P2-> appellation_label": {
        "s": get_all_veld_appellation_uri,
        "p": RDF.value,
        "o": get_all_veld_appellation_label,
    },
    "veld_instance -P1-> E42_instance": {
        "s": get_all_veld_uris,
        "p": CRM["P1_is_identified_by"],
        "o": get_all_veld_e42_uri,
    },
    "E42_instance -a-> E42": {
        "s": get_all_veld_e42_uri,
        "p": RDF.type,
        "o": CRM["E42_Identifier"],
    },
    "E42_instance -P190-> veld_instance": {
        "s": get_all_veld_e42_uri,
        "p": CRM["P190_has_symbolic_content"],
        "o": get_all_veld_urls,
    },
    "E42_instance -P2-> veld_instance": {
        "s": get_all_veld_e42_uri,
        "p": CRM["P2_has_type"],
        "o": CLS_LINK["documentation"],
    },
    
    # Tool Event Description
    "X13_instance -a-> X13": {
        "s": get_x13_per_code_or_chain_veld,
        "p": RDF.type,
        "o": CRMCLS["X13_Tool_Description"],
    },
    
    # Attribute Assignments Y8
    "E13_instance -a-> E13 (per Y8)": {
        "s": get_e13_per_veld_per_y8,
        "p": RDF.type,
        "o": CRM["E13_Attribute_Assignment"]
    },
    "E13_instance -P140-> veld_instance (per Y8)": {
        "s": get_e13_per_veld_per_y8,
        "p": CRM["P140_assigned_attribute_to"],
        "o": get_veld_uri_per_e13_per_y8,
    },
    "E13_instance -P134-> X13_instance (per Y8)": {
        "s": get_e13_per_veld_per_y8,
        "p": CRM["P134_continued"],
        "o": get_x13_per_e13_per_y8,
    },
    "E13_instance -P141-> method_instance (per Y8)": {
        "s": get_e13_per_veld_per_y8,
        "p": CRM["P141_assigned"],
        "o": get_method_per_e13_per_y8,
    },
    "E13_instance -P177-> Y8 (per Y8)": {
        "s": get_e13_per_veld_per_y8,
        "p": CRM["P177_assigned_property_of_type"],
        "o": CRMCLS["Y8_implements"],
    },

    # Attribute Assignments Y9
    "E13_instance -a-> E13 (per Y9)": {
        "s": get_e13_per_veld_per_y9,
        "p": RDF.type,
        "o": CRM["E13_Attribute_Assignment"]
    },
    "E13_instance -P140-> veld_instance (per Y9)": {
        "s": get_e13_per_veld_per_y9,
        "p": CRM["P140_assigned_attribute_to"],
        "o": get_veld_uri_per_e13_per_y9,
    },
    "E13_instance -P134-> X13_instance (per Y9)": {
        "s": get_e13_per_veld_per_y9,
        "p": CRM["P134_continued"],
        "o": get_x13_per_e13_per_y9,
    },
    "E13_instance -P141-> format_instance (per Y9)": {
        "s": get_e13_per_veld_per_y9,
        "p": CRM["P141_assigned"],
        "o": get_format_per_e13_per_y9,
    },
    "E13_instance -P177-> Y9 (per Y9)": {
        "s": get_e13_per_veld_per_y9,
        "p": CRM["P177_assigned_property_of_type"],
        "o": CRMCLS["Y9_expects_input"],
    },

    # Attribute Assignments Y10
    "E13_instance -a-> E13 (per Y10)": {
        "s": get_e13_per_veld_per_y10,
        "p": RDF.type,
        "o": CRM["E13_Attribute_Assignment"]
    },
    "E13_instance -P140-> veld_instance (per Y10)": {
        "s": get_e13_per_veld_per_y10,
        "p": CRM["P140_assigned_attribute_to"],
        "o": get_veld_uri_per_e13_per_y10,
    },
    "E13_instance -P134-> X13_instance (per Y10)": {
        "s": get_e13_per_veld_per_y10,
        "p": CRM["P134_continued"],
        "o": get_x13_per_e13_per_y10,
    },
    "E13_instance -P141-> format_instance (per Y10)": {
        "s": get_e13_per_veld_per_y10,
        "p": CRM["P141_assigned"],
        "o": get_format_per_e13_per_y10,
    },
    "E13_instance -P177-> Y10 (per Y10)": {
        "s": get_e13_per_veld_per_y10,
        "p": CRM["P177_assigned_property_of_type"],
        "o": CRMCLS["Y10_generates_output"],
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
    "RDF": "https://clscor.io/entity/type/method/applying_RDF_schema",
    "Testing": "https://clscor.io/entity/type/method/testing",
    "Bible Studies": "https://clscor.io/entity/type/method/applying_bible_studies",
    "Data Visualization": "https://clscor.io/entity/type/method/data_visualization",
    "Universal Dependencies": "https://clscor.io/entity/type/method/applying_universal_dependencies",
    "database": "https://clscor.io/entity/type/method/using_a_database",
    "demo": "https://clscor.io/entity/type/method/providing_a_demo",
    "triplestore": "https://clscor.io/entity/type/method/using_a_triplestore",
    "Analysis": "https://clscor.io/entity/type/method/corpus_analysis",
}