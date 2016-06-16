from SPARQLWrapper import SPARQLWrapper, JSON


def queryDBnary(server, lemma, pos, language):

    sparql = SPARQLWrapper(server)
    sparql.setQuery("""
    SELECT COUNT(distinct ?s) as ?numssenses WHERE {
    ?e a lemon:LexicalEntry;
        dcterms:language lexvo:"""+language+""";
        lemon:canonicalForm ?cf;
        lemon:sense ?s.
      ?cf lemon:writtenRep ?wf.
      FILTER(regex(?wf,"^"""+lemma+"""$","i"))
    }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    print(results)
    for result in results["results"]["bindings"]:
      return print(result["numssenses"]["value"])
      
    return 0
        #lexinfo:partOfSpeech lexinfo:"""+pos+""";
def queryDBnaryFull(server, lemma, pos, language):

    sparql = SPARQLWrapper(server)
    sparql.setQuery("""
PREFIX lexvo: <http://lexvo.org/id/iso639-3/>
SELECT ?wf, ?pos, ?numsenses WHERE {
SELECT ?wf, ?pos, COUNT(?s) as ?numsenses FROM <http://kaiko.getalp.org/dbnary/"""+language+"""> WHERE {
    ?e a lemon:LexicalEntry;
     dbnary:partOfSpeech ?pos;
     lemon:canonicalForm ?cf.
    ?cf lemon:writtenRep ?wf.
   ?e lemon:sense ?s.
}
GROUP BY ?wf ?pos ORDER BY ?wf 
}
LIMIT 10000
OFFSET 0
    """)
        #lemon:canonicalForm ?cf;
      #?cf lemon:writtenRep ?wf.
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    #print(results)
    limite=0
    while len(results["results"]["bindings"]) > 1:
        for result in results["results"]["bindings"]:
            print(result["wf"]["value"] + "\t" + result["pos"]["value"] + "\t"+ result["numsenses"]["value"])
        limite=limite+10000
        sparql.setQuery("""
PREFIX lexvo: <http://lexvo.org/id/iso639-3/>
SELECT ?wf, ?pos, ?numsenses WHERE {
SELECT ?wf, ?pos, COUNT(?s) as ?numsenses FROM <http://kaiko.getalp.org/dbnary/"""+language+"""> WHERE {
    ?e a lemon:LexicalEntry;
     dbnary:partOfSpeech ?pos;
     lemon:canonicalForm ?cf.
    ?cf lemon:writtenRep ?wf.
   ?e lemon:sense ?s.
}
GROUP BY ?wf ?pos ORDER BY ?wf 
}
LIMIT 10000
OFFSET """+str(limite)+"""
        """)        
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        
    #sparql = SPARQLWrapper(server)
    #sparql.setQuery("""
#PREFIX lexvo: <http://lexvo.org/id/iso639-3/>
#SELECT ?wf, ?pos, COUNT(?s) as ?numsenses FROM <http://kaiko.getalp.org/dbnary/fra> WHERE {
    #?e a lemon:LexicalEntry;
     #dbnary:partOfSpeech ?pos;
     #lemon:canonicalForm ?cf.
    #?cf lemon:writtenRep ?wf.
   #?e lemon:sense ?s.
#} GROUP BY ?wf ?pos ORDER BY ?wf 
#OFFSET 10000
#LIMIT 10000 
    #""")
        ##lemon:canonicalForm ?cf;
      ##?cf lemon:writtenRep ?wf.
    #sparql.setReturnFormat(JSON)
    #results = sparql.query().convert()
    #print(results)
    #for result in results["results"]["bindings"]:
        #print(result["numsenses"]["value"])
    #sparql.setQuery("""
#PREFIX lexvo: <http://lexvo.org/id/iso639-3/>
#SELECT ?wf, ?pos, COUNT(?s) as ?numsenses FROM <http://kaiko.getalp.org/dbnary/fra> WHERE {
    #?e a lemon:LexicalEntry;
     #dbnary:partOfSpeech ?pos;
     #lemon:canonicalForm ?cf.
    #?cf lemon:writtenRep ?wf.
   #?e lemon:sense ?s.
#} GROUP BY ?wf ?pos ORDER BY ?wf OFFSET 20000
    #""")
        ##lemon:canonicalForm ?cf;
      ##?cf lemon:writtenRep ?wf.
    #sparql.setReturnFormat(JSON)
    #results = sparql.query().convert()
    #print(results)
    #?e a lemon:LexicalEntry;
    #for result in results["results"]["bindings"]:
      #return print(result["numssenses"]["value"])
      
    return 0
        #lexinfo:partOfSpeech lexinfo:"""+pos+""";
"""		
SELECT COUNT(distinct ?s) as ?numssenses WHERE {
 ?e a lemon:LexicalEntry;
    dcterms:language lexvo:fra;
    lexinfo:partOfSpeech lexinfo:noun;
    lemon:canonicalForm ?cf;
    lemon:sense ?s.
   ?cf lemon:writtenRep ?wf.
   FILTER(regex(?wf,"^chat$","i"))
}
"""
if __name__ == "__main__":
    queryDBnaryFull("http://kaiko.getalp.org/sparql", "cat", "noun", "rus")
