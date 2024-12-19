from rdflib import Graph


IN_VELD_TTL_FILE = "./data/clscor_conversion/output.ttl"
IN_CLSCOR_FORMAT_FILE = "./data/clscor_conversion/clscor_vocabs/format.ttl"
IN_CLSCOR_METHOD_FILE = "./data/clscor_conversion/clscor_vocabs/method.ttl"
OUT_FORMAT_MISSING_FILE = "./data/clscor_conversion/clscor_vocabs/format_missing.txt"
OUT_FORMAT_MATCHED_FILE = "./data/clscor_conversion/clscor_vocabs/format_matched.txt"
OUT_METHOD_MISSING_FILE = "./data/clscor_conversion/clscor_vocabs/method_missing.txt"
OUT_METHOD_MATCHED_FILE = "./data/clscor_conversion/clscor_vocabs/method_matched.txt"


def compare(query_result_clscor, query_result_veld):
    set_clscor = {str(row[0]) for row in query_result_clscor}
    set_veld = {str(row[0]) for row in query_result_veld}
    set_missing_in_clscor = set_veld - set_clscor
    set_in_clscor = set_veld & set_clscor
    return set_missing_in_clscor, set_in_clscor


def write_to_txt(set_missing, file):
    list_missing_sorted = sorted(list(set_missing))
    with open(file, "w") as f:
        for m in list_missing_sorted:
            f.write(m + "\n")


def main():
    
    # load graph data
    g_clscor = Graph()
    g_veld = Graph()
    g_veld.parse(IN_VELD_TTL_FILE, format="turtle")
    g_clscor.parse(IN_CLSCOR_FORMAT_FILE, format="turtle")
    g_clscor.parse(IN_CLSCOR_METHOD_FILE, format="turtle")
    print(f"Loaded {len(g_clscor)} triples.")
    
    # compare formats
    query_clscor = """
    SELECT DISTINCT ?s
    WHERE {
      ?s rdf:type crmcls:X7_Format .
    }
    """
    query_veld = f"""
    SELECT DISTINCT ?o
    WHERE {{
      ?s ?p ?o .
      FILTER(STRSTARTS(STR(?o), "https://clscor.io/entity/type/format/"))
    }}
    """
    query_result_clscor = g_clscor.query(query_clscor)
    query_result_veld = g_veld.query(query_veld)
    set_missing_in_clscor, set_in_clscor = compare(query_result_clscor, query_result_veld)
    write_to_txt(set_missing_in_clscor, OUT_FORMAT_MISSING_FILE)
    write_to_txt(set_in_clscor, OUT_FORMAT_MATCHED_FILE)
    
    # compare methods
    query_clscor = """
    SELECT DISTINCT ?s
    WHERE {
      ?s rdf:type crmcls:X6_Method .
    }
    """
    query_veld = f"""
    SELECT DISTINCT ?o
    WHERE {{
      ?s ?p ?o .
      FILTER(STRSTARTS(STR(?o), "https://clscor.io/entity/type/method/"))
    }}
    """
    query_result_clscor = g_clscor.query(query_clscor)
    query_result_veld = g_veld.query(query_veld)
    set_missing_in_clscor, set_in_clscor = compare(query_result_clscor, query_result_veld)
    write_to_txt(set_missing_in_clscor, OUT_METHOD_MISSING_FILE)
    write_to_txt(set_in_clscor, OUT_METHOD_MATCHED_FILE)


if __name__ == "__main__":
    main()
