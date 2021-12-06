import pandas as pd

import numpy as np
import sys
import json

from rdflib.namespace import DC, DCTERMS, DOAP, FOAF, SKOS, OWL, RDF, RDFS, VOID, XMLNS, XSD
from rdflib import Graph, URIRef, Literal, Namespace
#JSON_file = pd.read_json(r'data/riedel_test.json', lines = True, chunksize = 10000)

def read_data(num_of_file):
   ''' This function returns the complete data fram created small dataset files and return as one by one'''
   for i in range(num_of_file):
        if i == 0:
            file = 'data/nyt/file1000.csv'
        elif i==num_of_file -1 :
            file = 'data/nyt/file172448.csv'
        else:
            file = 'data/nyt/file'+(str(i*1000))+'.csv'
        nyt_corpus = pd.read_csv(file, index_col=0)
   return nyt_corpus


g = Graph()

# Basic URIs
prop = Namespace("https://reld.dice-research.org/schema/")
res = Namespace("https://reld.dice-research.org/resource/")
datasetURI = Namespace("https://reld.dice-research.org/")

g.bind("dprop", prop)
g.bind("dres", res)
g.bind("dataset",datasetURI)


df = pd.DataFrame()


    
file = 'data/nyt/file170000.csv'
nyt_corpus = pd.read_csv(file, index_col=0)
nyt_corpus_relation = nyt_corpus['rel']
UValues = nyt_corpus_relation.unique()
sent_counter = 0
for index, r in enumerate(UValues):
    g.add((URIRef(res+"RE-NYT-Relation"+ str(index)),
           RDF.type, 
           URIRef(datasetURI+"NYT-FB")
           ))
    g.add((URIRef(res+"RE-NYT-Relation"+ str(index)),
           URIRef(prop+'relation'), 
           URIRef(res+r)
           ))
    one_relation_dataset = nyt_corpus[nyt_corpus.rel == r]
    USent = one_relation_dataset['sent'].unique()
    
    g.add((URIRef(res+'RE-NYT-Relation'+str(index)),
           URIRef(prop+'numSent'), 
           Literal(len(one_relation_dataset),lang='en')
           ))
    g.add((URIRef(res+'RE-NYT-Relation'+str(index)),
           URIRef(prop+'numUSent'), 
           Literal(len(USent),lang='en')
           ))
    
    for i, sent in enumerate(USent):
        sent_counter = sent_counter + 1
        g.add((URIRef(res+"RE-NYT-Relation"+ str(index)),
           URIRef(prop+'hasSentence'), 
           URIRef(res+'Sentence_'+str(sent_counter))
           ))
        g.add((URIRef(res+'Sentence_'+str(sent_counter)),
           URIRef(prop+'text'), 
           Literal(sent,lang='en')
           ))
        entity_sent_dataset = one_relation_dataset[one_relation_dataset.sent ==sent]
        g.add((URIRef(res+'Sentence_'+str(sent_counter)),
                   URIRef(prop+'numEntities'), 
                   Literal(len(entity_sent_dataset)*2,lang='en') # debatable because the entities might be same
                   ))
        for ind, s in entity_sent_dataset.iterrows():
            ###### Subject part ###############
            g.add((URIRef(res+'Sentence_'+str(sent_counter)),
                   URIRef(prop+'subject'), 
                   URIRef(res+'subject_'+str(ind)) # debatable because the entities might be same
                   ))
            g.add((URIRef(res+'subject_'+str(ind)),
                   URIRef(prop+'label'), 
                   URIRef(res+s['sub']) # can be litral I am leaving it intentioaly as IRI
                   ))
            g.add((URIRef(res+'subject_'+str(ind)),
                   URIRef(prop+'id'), 
                   URIRef(res+s['sub_id']) # Present in NYT but not in other dataset so also debateable
                   ))
            ###### Object part ###############
            ## Todo: 1) Look for the number of tokesn 2) Look for the NER 3) Look for the type of POS
            
            g.add((URIRef(res+'Sentence_'+str(sent_counter)),
                   URIRef(prop+'object'), 
                   URIRef(res+'object_'+str(ind)) 
                   ))
            g.add((URIRef(res+'object_'+str(ind)),
                   URIRef(prop+'label'), 
                   URIRef(res+s['obj']) 
                   ))
            g.add((URIRef(res+'object_'+str(ind)),
                   URIRef(prop+'id'), 
                   URIRef(res+s['obj_id']) 
                   ))
            
#     print(entity_sent_dataset.obj)
#     print(one_relation_dataset['sent'])
    

# # temp code
 
# # end temp code


g.serialize(destination="output/nyt_test_graph.ttl", format='ttl')
print("finished")
#<https://Name.dice-research.org/Wikidata-S1-rels>   https://Name.dice-research.org/schema/rel1        “dfsdfds sdf”