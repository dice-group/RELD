# -*- coding: utf-8 -*-
import urllib.parse
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import spacy
from spacy import displacy
NER = spacy.load("en_core_web_sm")
import spacy_dbpedia_spotlight
def encode_Url(query):
    return urllib.parse.quote_plus(query)
def build_sub_obj(subObj): # will convert it into urlEncode
    sub = subObj.strip().replace(" ","_")
    return sub



def entity_info_fewRel(entity_str, index, isNominal=False,sentence=""):
    
    entityDict = {}
    
    entityDict["entity"] = build_sub_obj(entity_str)
    #print(build_sub_obj(entity_str))
    if len(index):
        entityDict["isNominal"] = isNominal
        if type(index[0]) == list:
            entityDict["startIndex"] = index[0][0]
            entityDict["endIndex"] = index[0][-1]
        else:
            entityDict["startIndex"] = index[0]
            entityDict["endIndex"] = index[-1]
        if(isNominal == False):
            entityDict["sameAs"] = same_As(entity_str)
        else:
            entityDict["sameAs"] = []
    else:
        entityDict = entity_info(entity_str, sentence)
        
    return entityDict


def entity_info(entity_str,sentence,isNominal=False):
    """Input: subject= tokens of subject of a sentnece
    tokens= tokens of a sentneces as a list
    isNominal is optional it will only be true in case of semEval dataset
    
    return: subDict = dictionary of all the inforamtin about subject"""
    sentence = clean_sentence(sentence)
    entityDict = {}
    entityDict["entity"] = build_sub_obj(entity_str)
    #print(build_sub_obj(entity_str))
    entity = tokenize(entity_str.replace("_", " "))
    tokens = tokenize(sentence)
    entityDict["isNominal"] = isNominal
    for i in range(len(tokens)):
        if len(entity):
            if tokens[i].lower() == entity[0].lower():
                entityDict["startIndex"] = i
                
            if tokens[i].lower() == entity[-1].lower():
                entityDict["endIndex"] = i
                break
            else:
                if "startIndex" in entityDict.keys():    
                    entityDict["endIndex"] = entityDict["startIndex"]
        else:
            entityDict["startIndex"] = 0 
            entityDict["endIndex"] = 0
            
    if(isNominal == False):
        entityDict["sameAs"] = same_As(entity_str)
    else:
        entityDict["sameAs"] = []
    return entityDict

def tokens_info(sentence):
    tokensDict = {}     
    sentence = clean_sentence(sentence)
    tokens = tokenize(sentence)
   
    pos_tags = pos(tokens)
    punc = punctuation(tokens,sentence)
    tokensDict["tokens"] = tokens
    tokensDict["pos"] = pos_tags
    tokensDict["punct"] = punc
    
    return tokensDict

def tokens_info_wikiRe(tokens,sent):
    tokensDict = {}     
    
    pos_tags = pos(tokens)
    punc = punctuation(tokens,sent)
    tokensDict["tokens"] = tokens
    tokensDict["pos"] = pos_tags
    tokensDict["punct"] = punc
    
    return tokensDict

nlp = spacy.blank('en')
nlp.add_pipe('dbpedia_spotlight', config={'language_code': 'en'})

def same_As1(entity):
    """Input: entity= a named entity may ba a subject,object or named entity
    return: sameAs = a list of all the sameAs of available in other knowledge bases if found"""
    
    try:   
        doc = nlp(entity)
    #[(ent.text, ent.kb_id_, ent._.dbpedia_raw_result['@similarityScore']) for ent in doc.ents]
        return [ent.kb_id_ for ent in doc.ents]
    except:
        return []
import requests
def same_As(entity):    
    try:
        headers = {
            'Accept':'application/json'
        }
        data = {
            'text': entity,
            'confidence': '0.35',
            }
        response = requests.post('http://localhost:2222/rest/annotate', headers=headers, data=data)
        return [response.json()['Resources'][0]['@URI']]
    except:
        return []
    


def tokenize(string):
   return word_tokenize(string)

def pos(tokens):
    pos = []
    tokens_tag = pos_tag(tokens)
    for tag in tokens_tag:
        tag = tag[1]
        pos.append(tag)
    return pos

def punctuation(tokens,sentence):
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    new_words = tokenizer.tokenize(sentence)
    punct = [x for x in tokens if x not in new_words]
    return punct


def named_entities(sentnece):
    sentnece= NER(sentnece)
    nEntities = []
    for word in sentnece.ents:
        nEntities.append((build_sub_obj(remove_alphaNumeric(word.text).lower()),word.label_))
    return nEntities

def predicateProp(predicate,equivalent, isgenric=False):
    predDict = {}
    equ = []
    predDict["predicate"] = predicate
    predDict["isgenric"] = isgenric
    
    predDict["equivlant"] =  equ
    
    return predDict


import re
def containsNumber(string):
    if re.match(".*\\d+.*",string):
        return True
    else:
        return False

def clean_sentence(sentence):
    '''This function is mainly generated for SemEval dataset which uses <e1> and " '''
    if sentence.startswith('"'):
        sentence = sentence.split('"')[1]
    sentence = sentence.replace("<e1>", "" )
    sentence = sentence.replace("</e1>", "" )
    sentence = sentence.replace("<e2>", "" )
    sentence = sentence.replace("</e2>", "" )
    return sentence

import json
from urllib.request import urlopen
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

def remove_alphaNumeric(string):
    new_string = re.sub(r"[^a-zA-Z0-9_]+", ' ', string)
    new_string = new_string.strip().replace(" ", "_")
    if '__' in new_string:
        new_string = new_string.replace("__","_")
    return new_string

def get_max_str_index(lst):
    return max(enumerate(lst), key=lambda x: len(x[1]))[0]




#sent = "In June 1987 , the Missouri Highway and Transportation Department approved design location of a new four - lane Mississippi River bridge to replace the deteriorating Cape Girardeau Bridge ."
#entity_info("cape girardeau bridge", sent)
#t = "The Indian Space Research Organisation or is the national space agency of India, headquartered in Bengaluru. It operates under Department of Space which is directly overseen by the Prime Minister of India while Chairman of ISRO acts as executive of DOS as well."

# print(named_entities(t))

# print(same_As('India'))


    
#d = entity_info("Space_Research",t)

# sentence  = "Think and wonder, wonder 1988w and think."
# punc = tokenize(sentence)

# tokenizer = nltk.RegexpTokenizer(r"\w+")
# new_words = tokenizer.tokenize(sentence)
# punct = [x for x in punc if x not in new_words]

#d = tokens_info(t)

#print(d)


# # normal loading
# import spacy
# nlp = spacy.blank('en')
# # when loading the pipeline, specify the debug option
# nlp.add_pipe('dbpedia_spotlight', config={'debug': True})
# # now try performing the entity recognition/linking and take a look at the logs
# nlp('Is everything working ok?').ents
