from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS

from src.convert_to_clscor import *


PEM = Namespace("http://parthenos.d4science.org/CRMext/CRMpe.rdfs")
CRMCLS = Namespace("https://clscor.io/ontologies/CRMcls/")


mappings = {
    "data_uri a PE19": {
        "s": get_data_veld_uris,
        "p": RDF.type,
        "o": PEM["PE19_Persistent_Digital_Object"],
    },
    "code_uri a PE23": {
        "s": get_code_veld_uris,
        "p": RDF.type,
        "o": PEM["PE23_Volatile_Software"],
    },
    "code_uri a X12": {
        "s": get_code_veld_uris,
        "p": RDF.type,
        "o": CRMCLS["X12_Tool"],
    },
    "chain_uri a X5": {
        "s": get_chain_veld_uris,
        "p": RDF.type,
        "o": CRMCLS["X5_Research_Activity"],  # questionable
    },
    "chain_uri a PE23": {
        "s": get_chain_veld_uris,
        "p": RDF.type,
        "o": PEM["PE23_Volatile_Software"],
    },
    "code_uri a X12": {
        "s": get_code_veld_uris,
        "p": RDF.type,
        "o": CRMCLS["X12_Tool"],
    },
    "chain_uri crmcls:Y7_uses code_uri": {
        "s": get_chain_veld_uris,
        "p": CRMCLS["Y7_uses"],
        "o": get_integrated_code_veld_id,
    },
    "chain_uri hadInput data_uri": {
        "s": get_chain_veld_uris,
        "p": CRMCLS["hadInput"],
        "o": get_data_veld_uris__as_chain_input,
    },
    "chain_uri generatedOutput data_uri": {
        "s": get_chain_veld_uris,
        "p": CRMCLS["generatedOutput"],
        "o": get_data_veld_uris__as_chain_output,
    },
    "chain_uri type X6": {
        "s": get_chain_veld_uris,
        "p": CRMCLS["type"],
        "o": get_chain_topic_as_x6,
    },
    "code_uri crmcls:Y8_implements X6": {
        "s": get_code_veld_uris,
        "p": CRMCLS["Y8_implements"],
        "o": get_code_topic_as_x6,
    },
}
