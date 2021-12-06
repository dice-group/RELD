# -*- coding: utf-8 -*-

import re
from random import randint
from dateutil.parser import parse
import json
from urllib.request import urlopen
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

def returnValue(dict, search):
    for key, value in dict.items():
        if value == search:
            return key


def get_id(relation_counter, sentence_counter):
    rand = randint(0, 1000)
    num = relation_counter + sentence_counter + rand
    ids = ""+str(num)+""+str(relation_counter) +""+str(sentence_counter)
    return ids

def is_date(string, fuzzy=False):
    try: 
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False
def check_type(string):
    if bool(re.match('^[0-9\.]*$', string)):
        return True
    else:
        False

def remove_alphaNumeric(string):
    new_string = re.sub(r"[^a-zA-Z0-9_]+", ' ', string)
    new_string = new_string.strip().replace(" ", "_")
    if '__' in new_string:
        new_string = new_string.replace("__","_")
    return new_string

def containsNumber(string):
    if re.match(".*\\d+.*",string):
        return True
    else:
        return False
    
def id_to_name(Fid):
    url = "http://sameas.org/store/freebase/json?uri=http://rdf.freebase.com/ns/m." + Fid
    name = ""
    retriveUrl = []
    response = urlopen(url)
    data_json = json.loads(response.read())
    retriveUrl = data_json[0]['duplicates'][0].split("/")
    if len(retriveUrl) > 4 and "dbpedia.org" in retriveUrl[2]:
        name = retriveUrl[4]
    else:
        name = Fid
    return name
def clean_sentences(string,e1,e2):
    s = []
    string = string.replace('"', '')
    string = string.replace('.','')
    
    string = string.split(' ')
    for w in string:
        if w.strip() == '<e1>'+e1.strip()+'</e1>':
            w = e1
        elif  w.strip() == '<e2>'+e1.strip()+'</e2>':
            w = e1
        elif w.strip() == '<e1>'+e2.strip()+'</e1>':
            w = e2
        elif w.strip() == '<e2>'+e2.strip()+'</e2>':
            w = e2
       
        s.append(w)
    listToStr = ' '.join(map(str, s))

    return listToStr
    

def wikidata_id_toText(ids):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    text = ""
    query = """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
               PREFIX wd: <http://www.wikidata.org/entity/> 
                    SELECT  ?item 
                        WHERE {
                            wd:"""+ids+""" rdfs:label ?item .
                            FILTER (langMatches( lang(?item), "EN" ) )
                            } 
                        LIMIT 1 """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    text = results['results']['bindings'][0]['item']['value']
    if text == "":
        return ids
    else:
        return text


#print(wikidata_id_toText('P364'))

# SELECT ?item ?itemLabel
#                     WHERE
#                     {
#                         ?item wdt:P31 wd:Q146 .
#                         SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
#                         }
    
