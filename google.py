# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import csv

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
output = {}
subject_dict = {}
object_dict = {}
path = 'data/google/'

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

def structured_data(path):
    #data_all = pd.DataFrame()
    df_list = []
    subject_counter = 0
    obj_counter = 0
    dist = 'train'
    for filename in os.listdir(path):
        if not filename.endswith('.json'): continue
        
        fullname = os.path.join(path, filename)
        if fullname == 'data/test/institution_clean.json':
            d_temp = pd.read_json (r''+ fullname, lines=True)
            df_list.append(d_temp.T)
            #data_all = data_all.append(data.T, ignore_index=True)
        else:
            d_temp = pd.read_json (r''+ fullname, lines=True)
            df_list.append(d_temp)
    data = pd.concat(df_list, ignore_index=True)
    
    for i in range(len(data)):
        lst_all = []
        sentence = []
        
        sub = data['sub'][i].split('/')
        sub = id_to_name(sub[2])
        if containsNumber(data['obj'][i]):
            obj = data.obj[i]
        else:
            obj = id_to_name(data['obj'][i].split('/')[2])
        sent0 = data['evidences'][i]
        sent = sent0[0]
        sent = sent['snippet']
        sentence.append((sent,s.tokenize(sent, sub.replace('_',' '),obj.replace('_',' '))))
        if sub in subject_dict:
            sub = subject_dict[sub]
        else:
            subject_dict[sub] = subject_counter
            sub = subject_counter
            subject_counter = subject_counter + 1
        if obj in object_dict:
            obj = object_dict[obj]
        else:
            object_dict[obj] = obj_counter
            obj = obj_counter
            obj_counter = obj_counter + 1
        tup = (sub,obj,sentence,1,dist)
        lst_all.append(tup)
        relation = data.pred[i].split('/')
        relation = relation[len(relation) -1]
        if relation in output:
            
            output[relation].extend(lst_all)
        else:
            output[relation] = lst_all
    return output, subject_dict, object_dict


def create_rdf(output,dsName):
    sent_counter = 0
    relation = ""
    ne_counter = 0
    list_Others = ['P0', "P7" , 'P9' ,"P134" , "P1962"]
    relation_text = ""
    sent_id = ""
    rel_data = pd.read_csv("data/AllRelationWithCrossCheck.csv")
    g.add((URIRef(res+"Dataset_1"), # will go to all code
           #URIRef(prop+'name'),
           DC.title, 
           URIRef(res+dsName)
           ))
    g.add((URIRef(res+dsName),
           URIRef(prop+'primaryTask'), 
           URIRef(res+'RE')
           ))
    g.add((URIRef(res+dsName),
           DC.source, 
           URIRef(res+'Wikipedia_freebase')
           ))
    g.add((URIRef(res+dsName),
           URIRef(prop+'reType'), 
           URIRef(res+'binary')
           ))
    for i, (rel,info) in enumerate(output.items()):
        #rel = rel[0]
        print(rel)
        ID = rel_data.loc[rel_data['RE-Google-Relation'] == rel, 'Grid'].iloc[0]
        print(ID)
        relation = res+"R-"+str(ID)
        g.add((URIRef(datasetURI+dsName),
                   URIRef(prop+"hasRelation"), 
                   URIRef(relation)
                   ))
        if rel in list_Others:
            rel == 'RE-Google-Relation_Other'
            g.add((URIRef(res+""+rel),
               RDFS.label, 
               Literal("Other")
               ))
            # g.add((URIRef(datasetURI+dsName),
            #        URIRef(prop+"hasRelation"), 
            #        URIRef(rel)
            #        ))
        else:
            relation_text = rel#rel_data.loc[rel_data['WikidataIds'] == rel, 'RE-WikiRE-Relation'].iloc[0] 
            # relation_id = relation_text.replace(' ','_')
            # relation_id = res+"RE-FewRel-Relation_"+relation
            
           
            g.add((URIRef(relation),
                   RDFS.label, 
                   Literal(relation_text)
                   ))
        # # Testing code
        # relation_id = rel_data.loc[rel_data['WikidataIds'] == rel, 'Rid'].iloc[0]
        # g.add((URIRef(relation), # This will go to the iamge and ontology
        #       URIRef(prop+'relationId'),
        #       URIRef(res+""+relation_id)
        #       ))
        # end Testing code
        wr = rel_data.loc[rel_data['RE-Google-Relation'] == rel, 'WikidataIds'].iloc[0]
        if str(wr) != 'nan':
            g.add((URIRef(relation), # This property only is used for fewRel and wikire
                    OWL.sameAs, 
                    URIRef(wikidata+wr)
                    ))
        fb = rel_data.loc[rel_data['RE-Google-Relation'] == rel, 'freebase'].iloc[0]
        if str(fb) != 'nan':
            g.add((URIRef(relation), # freebase
              OWL.sameAs, 
              URIRef(freebase+fb)
              ))
        wikire = rel_data.loc[rel_data['RE-Google-Relation'] == rel, 'RE-WikiRE-Relation'].iloc[0]
        if str(wikire) != 'nan':
            wikireid = rel_data.loc[rel_data['RE-WikiRE-Relation'] == wikire, 'Wrid'].iloc[0]
            g.add((URIRef(relation), # wikiRE
              OWL.sameAs, 
              URIRef(res+"R-"+str(wikireid))
              ))
        few = rel_data.loc[rel_data['RE-Google-Relation'] == rel, 'RE-FewRel-Relation'].iloc[0]
        if str(few) != 'nan':
            fewid = rel_data.loc[rel_data['RE-FewRel-Relation'] == few, 'Frid'].iloc[0]
            g.add((URIRef(relation), # wikiRE
              OWL.sameAs, 
              URIRef(res+"R-"+str(fewid))
              ))
        nyt = rel_data.loc[rel_data['RE-Google-Relation'] == rel, 'RE-NYT-Relation'].iloc[0]
        if str(nyt) != 'nan':
            nytid = rel_data.loc[rel_data['RE-NYT-Relation'] == nyt, 'Nrid'].iloc[0]
            g.add((URIRef(relation), # nyt
              OWL.sameAs, 
              URIRef(res+"R-"+str(nytid))
              ))
        nlg = rel_data.loc[rel_data['RE-Google-Relation'] == rel, 'RE-WebNLG-Relation'].iloc[0]
        if str(nlg) != 'nan':
            nlgid = rel_data.loc[rel_data['RE-WebNLG-Relation'] == nlg, 'Wgrid'].iloc[0]
            g.add((URIRef(relation), # webnlg
              OWL.sameAs, 
              URIRef(res+"R-"+str(nlgid))
              ))
        # google = rel_data.loc[rel_data['RE-Google-Relation'] == rel, 'RE-Google-Relation'].iloc[0]
        # if str(google) != 'nan':
        #     googleid = rel_data.loc[rel_data['RE-Google-Relation'] == google, 'Grid'].iloc[0]
        #     g.add((URIRef(relation), # google
        #       OWL.sameAs, 
        #       URIRef(res+"R-"+str(googleid))
        #       ))
        equal = rel_data.loc[rel_data['RE-Google-Relation'] == rel, 'owl:equivalentProperty'].iloc[0]
        if str(equal) != 'nan':
            g.add((URIRef(relation), # equivalent Property
              OWL.equivalentProperty, 
              URIRef(res+""+str(equal).strip().replace(" ", "_"))
              ))
        for index, val in enumerate(info): # Code for Sentence and relevant info
           
            g.add((URIRef(relation),
                   URIRef(prop+'distribution'), 
                   Literal(val[4],datatype=XSD.string)
                   ))
            
            for ind, v in enumerate(val[2]):
                sent_id = res+"S_"+dsName+"_"+ str(sent_counter) # will go to all code
                sent_counter = sent_counter + 1
                g.add((URIRef(relation),
                   URIRef(prop+'hasSentence'), 
                   URIRef(sent_id)
                ))
                g.add((URIRef(sent_id),
                       URIRef(prop+'hasText'), 
                       Literal(v[0],lang='en')
                       ))
                for key , value in v[1].items(): # code for named entities
                    if key == "listOfNamedEntities":
                        for nam_e in value:
                            ne_id = res+'ne_g' + str(ne_counter)
                            #ne_id = res+ str(nam_e[0]).strip().replace(' ','_')+str(ne_counter)
                            ne_counter = ne_counter + 1
                            g.add((URIRef(sent_id),
                                    URIRef(prop+'hasNamedEntity'), 
                                    URIRef(ne_id)
                            ))
                            g.add((URIRef(ne_id),
                                   RDF.type,
                                   URIRef(dbo+remove_alphaNumeric(nam_e[1]))
                                   ))
                            g.add((URIRef(ne_id),
                                   RDFS.label,
                                   Literal(nam_e[0],lang='en')
                                   ))
                    else:
                        g.add((URIRef(sent_id),
                               URIRef(prop+key), 
                               Literal(value,datatype=XSD.integer)
                               ))
            ################ Subject Object Code ##################
            g.add((URIRef(sent_id),
                   URIRef(prop+'numOfRelation'), 
                   Literal(val[3],datatype=XSD.integer) 
                   )) 
            subject_string = returnValue(subject_dict,val[0])
            g.add((URIRef(sent_id),
                   URIRef(prop+'hasSubject'), 
                   URIRef(res+'subject_'+str(val[0])) 
                   ))
            if containsNumber(str(subject_string)):
                g.add((URIRef(res+'subject_'+str(val[0])),
                       RDFS.label, 
                       Literal(subject_string,datatype=XSD.string) 
                       ))
          
            
            elif check_type(str(subject_string)):
                g.add((URIRef(res+'subject_'+str(val[0])),
                       RDFS.label, 
                       Literal(subject_string,datatype=XSD.string))) 
                
            else:
                g.add((URIRef(res+'subject_'+str(val[0])),
                       URIRef(prop+'subject'), 
                       URIRef(res+ remove_alphaNumeric(subject_string))))
            object_string = returnValue(object_dict,val[1])#remove_alphaNumeric(val[1]) 
            g.add((URIRef(sent_id),
                   URIRef(prop+'hasObject'), 
                   URIRef(res+'object_'+str(val[1])) 
                   ))
            if containsNumber(str(object_string)):
                g.add((URIRef(res+'object_'+str(val[1])),
                       RDFS.label, 
                       Literal(object_string,datatype=XSD.string) # debatable because the entities might be same
                       ))
            
            elif check_type(str(object_string)):
                g.add((URIRef(res+'object_'+str(val[1])),
                    RDFS.label, 
                    Literal(object_string,datatype=XSD.string) 
                    ))
            else:
                g.add((URIRef(res+'object_'+str(val[1])),
                       URIRef(prop+'object'), 
                       URIRef(res+ remove_alphaNumeric(object_string)) # debatable because the entities might be same
                       ))
    g.serialize(destination="output/google/google_231121_final.ttl", format='ttl')
    print(f"finished with sentence length = {sent_counter} and NE length = {ne_counter} and graph = {len(g)}")
    

def main():
   
    dataset_Name = "Google_RE" 
    structured_data(path)
    print("The output = "+str(len(output)))
    create_rdf(output,dataset_Name)

if __name__ == "__main__":
    main()