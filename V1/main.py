# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
import csv
import xmltodict
import sys
import json
from urllib.request import urlopen
from dateutil.parser import parse
from rdflib.namespace import DC, DCTERMS, DOAP, FOAF, SKOS, OWL, RDF, RDFS, VOID, XMLNS, XSD
from rdflib import Graph, URIRef, Literal, Namespace # here is some error
import time
import re
import os
from random import randint
import sentence as s
from  validate import containsNumber , returnValue, check_type, remove_alphaNumeric, is_date, clean_sentences ,wikidata_id_toText, id_to_name
import webNlg 
import google 
import semEval
import wikiRE
import few_rel
import NYT_New


from datetime import datetime



g = Graph()


#re_types = ['binary', 'ternary','Joint_entity_re','overlapping','qa_re','bio_re','fewshot','slot_filling','multilangual' ,'Document']
# Basic URIs
prop = Namespace("https://reld.dice-research.org/schema/")
res = Namespace("https://reld.dice-research.org/resource/")
datasetURI = Namespace("https://reld.dice-research.org/")
dbo = Namespace("http://dbpedia.org/ontology/")
freebase = Namespace("http://rdf.freebase.com/ns")
wikidata = Namespace("http://www.wikidata.org/prop/statement/")
owl = Namespace("http://www.w3.org/2002/07/owl#")
dc = Namespace("http://purl.org/dc/elements/1.1/")

g.bind("reldv", prop)
g.bind("reldr", res)
g.bind("dataset",datasetURI)
g.bind("dbo",dbo)
g.bind("ps",wikidata)
g.bind('freebase',freebase)
g.bind('owl',owl)
g.bind('dc',dc)


def main():
    list_dataset = ["WebNLG", "Google_RE", "NYT-FB", "FewRel", "SemEval" ,"Wiki-RE"]
    for x in list_dataset:
        subject_dict = {}
        object_dict = {}
        output = {}
        if x == "WebNLG":
            path = 'data/WebNLG/'
            output, subject_dict, object_dict = webNlg.structured_data(path)
            print("The Number of Relations in "+x+" = "+str(len(output)))
            webNlg.create_rdf(output,x,subject_dict, object_dict)
            
        elif x == "Google_RE":
            path = 'data/google/'
            output, subject_dict, object_dict = google.structured_data(path)
            print("The Number of Relations in "+x+" = "+str(len(output)))
            google.create_rdf(output,x,subject_dict, object_dict)
        elif x == "SemEval":
            path = 'data/SemEval/'
            output, subject_dict, object_dict = semEval.structured_data(path)
            print("The Number of Relations in "+x+" = "+str(len(output)))
            semEval.create_rdf(output,x,subject_dict, object_dict)
        elif x == "NYT-FB":
            path = 'data/NYT_New/'
            output, subject_dict, object_dict = NYT_New.structured_data(path)
            print("The Number of Relations in "+x+" = "+str(len(output)))
            NYT_New.create_rdf(output,x,subject_dict, object_dict)
        elif x == "FewRel":
            path = 'data/fewrel/'
            output, subject_dict, object_dict = few_rel.structured_data(path)
            print("The Number of Relations in "+x+" = "+str(len(output)))
            few_rel.create_rdf(output,x,subject_dict,object_dict)
        else:
            path = 'data/wikiRe/'
            output, subject_dict, object_dict = wikiRE.structured_data(path)
            print("The Number of Relations in "+x+" = "+str(len(output)))
            wikiRE.create_rdf(output,x,subject_dict,object_dict)

if __name__ == "__main__":
    main()

