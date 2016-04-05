# -*- coding: utf-8 -*-

from SPARQLWrapper import SPARQLWrapper, JSON
import ast

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
def queryDBnaryFull(server, language_code_iso, language_code_dbnary):

    fcorresp=open("corresp."+language_code_iso,"r")
    line=fcorresp.readline()
    line=fcorresp.readline().strip()
    dict_corresp=ast.literal_eval(line)
    fdict=open("dictionnary."+language_code_iso,"w")
    sparql = SPARQLWrapper(server)
    sparql.setQuery("""
PREFIX lexvo: <http://lexvo.org/id/iso639-3/>
SELECT ?wf, ?pos, ?numsenses WHERE {
SELECT ?wf, ?pos, COUNT(?s) as ?numsenses FROM <http://kaiko.getalp.org/dbnary/"""+language_code_dbnary+"""> WHERE {
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
            if result["pos"]["value"] in dict_corresp:
                rep_pos=dict_corresp[result["pos"]["value"]]
            else:
                rep_pos="<unknown>"
            fdict.write(result["wf"]["value"] + "\t" + rep_pos + "\t"+ result["numsenses"]["value"]+"\n")
        limite=limite+10000
        sparql.setQuery("""
PREFIX lexvo: <http://lexvo.org/id/iso639-3/>
SELECT ?wf, ?pos, ?numsenses WHERE {
SELECT ?wf, ?pos, COUNT(?s) as ?numsenses FROM <http://kaiko.getalp.org/dbnary/"""+language_code_dbnary+"""> WHERE {
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

    fdict.close()        
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
    langex=["eng","fra","rus","spa","deu"]
    langsh=["en","fr","ru","es","de"]
    langex=["eng","fra","spa"]
    langsh=["en","fr","es"]
    for i  in range(0,len(langsh)):
      print("Extraction of the dictionnary for language "+langsh[i])
      queryDBnaryFull("http://kaiko.getalp.org/sparql", langsh[i], langex[i])
