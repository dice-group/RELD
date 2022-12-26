# -*- coding: utf-8 -*-
from nltk.tokenize import word_tokenize 
from nltk import pos_tag
import spacy
nlp = spacy.load('en_core_web_sm')


        
def ner(sentence):
    ner_lst = []
    doc = nlp(sentence)
    for ent in doc.ents:
        
        ner_lst.append((ent.text,ent.label_))
        #print(ent.text, ent.start_char, ent.end_char, ent.label_)
    return ner_lst   
def tokenize(sentence,entity_sub, entity_obj):
    sentence_dict = {}
    punct_count = 0
    pos_sub = 0 
    pos_obj = 0
    before = 0
    after = 0
    between = 0
    direction = False
    sentence = sentence.lower()
    
    entity_sub = entity_sub.lower().split(' ')
    entity_obj = entity_obj.lower().split(' ')
    NE = ner(sentence)
    #sentence_dict["numOfNamedEntities"] = len(NE)
    sentence_dict["listOfNamedEntities"] = NE
    
    sentence_dict["numOfSubToken"] = len(entity_sub)
    sentence_dict["numOfObjToken"] = len(entity_obj)
    
    list_of_tokens = word_tokenize(sentence)
    #tags = pos_tag(list_of_tokens)
    #sentence_dict["pos"] = tags
    num_of_tokens = len(list_of_tokens)
    #sentence_dict["tokens"] = list_of_tokens
    sentence_dict["numOfTokens"] = num_of_tokens
    if entity_sub[0] in list_of_tokens:
        pos_sub = list_of_tokens.index(entity_sub[0])
        sentence_dict["subPos"] = pos_sub
        #sentence_dict["sub_n_token"] = len(entity_sub.split(' '))
        
        
    if entity_obj[0] in list_of_tokens:
        pos_obj = list_of_tokens.index(entity_obj[0])
        sentence_dict["objPos"] = pos_obj
        #sentence_dict["obj_n_token"] = len(entity_obj.split(' '))
    
    for x in list_of_tokens:
        if x in ('!', "," ,"\'" ,";" ,"\"", ".", "-" ,"?"):
            punct_count = punct_count + 1
    sentence_dict["numOfPunctuations"] = punct_count
    
    if (pos_sub < pos_obj):
        before = pos_sub
        after = len(list_of_tokens) - (pos_obj + len(entity_obj))
        between = pos_obj - (pos_sub + len(entity_sub))
        direction = False
        
    else:
        before = pos_obj
        direction = True
        after = len(list_of_tokens) - (pos_sub + len(entity_sub))
        between = abs(pos_sub - (pos_obj + len(entity_obj)))
        
    
    sentence_dict["numBefToken"] = before
    sentence_dict["numAftToken"] = after
    sentence_dict["numBetToken"] = between
    sentence_dict["direction"] = direction
     
    return sentence_dict


Sentence = "Alan Bean was born in Wheeler, Texas and is from the U.S. He graduated in 1955 from UT Austin with a B.S. He worked as a test pilot and for NASA in 1963. He spent 100305 minutes in space and is now retired."
entity_sub = 'Alan Bean'
entity_obj = 'Test pilot'

# #print(num_of_punctuation(Sentence))
dic = tokenize(Sentence,entity_sub,entity_obj)


class Sentence:
    def __init__(self, sent, num_of_tokens, list_of_tokens, num_punctuations, sub_position, obj_position, before_tokens, between_tokens, after_tokens):
        self.sent = sent
        self.num_of_tokens = num_of_tokens
        self.list_of_tokens = list_of_tokens
        self.num_punctuations = num_punctuations
        self.sub_position = sub_position
        self.obj_position = obj_position
        self.before_tokens = before_tokens
        self.between_tokens = between_tokens
        self.after_tokens = after_tokens






