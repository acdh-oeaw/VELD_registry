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
        "o": get_code_ved__file_type_inputs,
    },
    "code veld Y10 X7": {
        "s": get_code_veld_uris,
        "p": CRMCLS["Y10_generates_output"],
        "o": get_code_ved__file_type_outputs,
    },
    "code veld url a X12": {
        "s": get_code_veld_uris,
        "p": RDF.type,
        "o": CRMCLS["X12_Tool"],
    },
    "code veld url crmcls:Y8_implements X6": {
        "s": get_code_veld_uris,
        "p": CRMCLS["Y8_implements"],
        "o": get_code_topic_as_x6,
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
    "chain veld url crmcls:Y8_implements X6": {
        "s": get_chain_veld_uris,
        "p": CRMCLS["Y8_implements"],
        "o": get_chain_topic_as_x6,
    },
    "chain veld url rdfs:label label": {
        "s": get_chain_veld_uris,
        "p": RDFS.label,
        "o": get_chain_veld_label,
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