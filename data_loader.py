# -*- coding: utf-8 -*-
import os
import utils as u
import pandas as pd
import json
from rdflib import Graph, URIRef, Literal, Namespace # here is some error
from rdflib.namespace import DC, DCTERMS, OWL, RDF, RDFS, VOID, XMLNS, XSD, PROV

    
g = Graph()
from tqdm import tqdm
reldp = Namespace("http://reld.dice-research.org/property/")
prop = Namespace("http://reld.dice-research.org/schema/")
res = Namespace("http://reld.dice-research.org/resource/")
#datasetURI = Namespace("https://reld.dice-research.org/")
dbo = Namespace("http://dbpedia.org/ontology/")
freebase = Namespace("http://rdf.freebase.com/ns")
wikidata = Namespace("http://www.wikidata.org/prop/statement/")
owl = Namespace("http://www.w3.org/2002/07/owl#")
dc = Namespace("http://purl.org/dc/elements/1.1/")
dcterms = Namespace("http://purl.org/dc/terms/")
nif = Namespace("http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#")
prov = Namespace("http://www.w3.org/ns/prov#")
dbpedia = Namespace("http://dbpedia.org/property/")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
schema = Namespace("http://schema.org/")
dicom = Namespace("http://purl.org/healthcarevocab/v1")
dcat = Namespace("http://www.w3.org/ns/dcat")
bibtex = Namespace("http://purl.org/net/nknouf/ns/bibtex#")
prof = Namespace("http://www.w3.org/ns/dx/prof/")
dbr = Namespace("http://dbpedia.org/resource/")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
g.bind("reld", prop)
g.bind("reldr", res)
g.bind("dcterms",dcterms)
g.bind("dbo",dbo)
g.bind("ps",wikidata)
g.bind('freebase',freebase)
g.bind('owl',owl)
g.bind('dbo',dbpedia)
g.bind('rdf',rdf)
g.bind('prov',prov)
g.bind('dc',dc)
g.bind('nif',nif)
g.bind('schema',schema)
g.bind('dicom',dicom)
g.bind('dcat',dcat)
g.bind('bibtex',bibtex)
g.bind('prof',prof)
g.bind('dbr',dbr)
g.bind('rdfs',rdfs)
g.bind('reldp',reldp)
def resource(S,P,O,R=True):
    if R:
        try:
            g.add((URIRef(S),
                   P, 
                   URIRef(O)
                   ))
        except AssertionError:
            g.add((URIRef(S),
                   URIRef(P), 
                   URIRef(O)
                   ))
                       
    else:
        try:
            g.add((URIRef(S),
                   P,
                   Literal(O[0],datatype=O[1])               
                   ))
        except AssertionError:
            g.add((URIRef(S),
                   URIRef(P),
                   Literal(O[0],datatype=O[1])               
                   ))

class Dataset:
    title = ""
    url = ""
    knownfor = ""
    dsType = ""
    lang = ""
    def __init__(self,title,url, kfor,dtype,lang):
        self.title = title
        self.url = url
        self.knownfor = kfor
        self.dsType = dtype
        self.lang = lang
    def dataset_rdf(self,counter):
        ds = res+"ds_"+counter
        resource(ds, RDF.type, prop+"Dataset")
        resource(ds, DC.title, (self.title,XSD.string),False)
        resource(ds,schema+'url',self.url)
        resource(ds,dbo+'knownFor',(self.knownfor,XSD.string),False)
        resource(ds,DCTERMS.language,(self.lang,XSD.string),False)
        resource(ds,dicom+'datasetType',(self.dsType,XSD.string),False)
        return ds
    
class String:
    distribution = "" 
    strType = ""
    def __init__(self, distribution,strtype):
       #self.objFollowSub = objFSub
        self.distribution = distribution
        self.strType = strtype
    def string_rdf(self,counter,ds): 
        st = res+"S-"+str(counter)
        resource(st, PROV.hadPrimarySource, ds)
        resource(st, RDF.type,nif+"String")
        resource(st, dcat+'distribution', (self.distribution,XSD.string),False)
        resource(st,prop+'strType',(self.strType,XSD.string),False)
        return st
    def string_doc_rdf(self,counter,ds,numSent,title):
        st = self.string_rdf(counter,ds)
        resource(st, prop+'numSent', (numSent,XSD.int),False)
        resource(st, bibtex+'hasTitle', (title,XSD.string),False)
        return st
class Token_Pos_Punct:
    posSeq = []
    tokens = []
    punc = []
    string = ""
    
    def __init__(self,dictTokens,string):
        self.posSeq = dictTokens['pos']
        self.tokens = dictTokens['tokens']
        self.punc = dictTokens['punct']
        self.string = string
        
    def tokens_rdf(self,counter):
        tokenId = res+"token_"+str(counter)
        posId = res+"posSeq"+str(counter)
        puncId = res+"puncSeq"+str(counter)
        
        resource(tokenId,RDF.type,prop+"Token")
        resource(self.string,prof+"hasToken",tokenId)
        resource(posId,RDF.type,prop+"POS")
        resource(self.string,res+"hasPOS",posId)
        resource(puncId,RDF.type,prop+"Punctuation")
        resource(self.string,res+"hasPunctuation",puncId)
        
        if(len(self.tokens) > 0 ):
            for i, tok in enumerate(self.tokens):
                resource(tokenId,rdf+'_'+ str(i),(tok,XSD.token),False)
        if(len(self.posSeq) > 0 ):
            for i, pos in enumerate(self.posSeq):
                resource(posId,rdf+'_'+str(i), (pos,XSD.string),False)
        if(len(self.punc) > 0 ):
            for i, p in enumerate(self.punc):
                resource(puncId, rdf+'_'+str(i), (p,XSD.string),False)
        return tokenId     
            
class Statement:
    
    stringObj = None
    def __init__(self,stringObj):
        self.stringObj = stringObj
        
    def statement_rdf(self,counter,stmt_count,subFobj,meta_data): 
        statment = res+"Stmt"+str(counter)+""+str(stmt_count)
        resource(self.stringObj,prop+'hasStatement',statment)
        resource(statment,RDF.type,RDF.Statement)
        resource(statment,prop+'subFollowObj',(subFobj,XSD.boolean),False) 
        if meta_data:
            for k,v in meta_data.items():
                resource(statment,k,(v,XSD.string),False)
        return statment
#meta data info
class Subject:
    stmt = None
    subject = ""
    startIndex = 0
    endIndex = 0
    isNominal = False
    sameAs = []
    
    def __init__(self,stmt,subDict):
        self.stmt = stmt
        self.subject = subDict["entity"]
        if "startIndex" in subDict.keys():
            self.startIndex = subDict["startIndex"]
        else:
            self.startIndex = 0
        if "endIndex" in subDict.keys():
            self.endIndex = subDict["endIndex"]
        else:
            self.endIndex = 0
        self.isNominal = subDict["isNominal"]
        self.sameAs = subDict["sameAs"]
            
    def subject_rdf(self): 
        sub = res+""+self.subject.lower()
        resource(self.stmt, RDF.subject, sub)
        resource(sub,RDF.type,RDFS.Resource)
    
        if(self.isNominal):
            resource(sub,prop+'isNominal',(self.isNominal,XSD.boolean),False)
        resource(self.stmt, prop+'subStartIndex', (self.startIndex,XSD.integer),False)
        resource(self.stmt, prop+'subEndIndex', (self.endIndex,XSD.integer),False)
        resource(sub,RDFS.label,(self.subject,XSD.string),False)
        if(len(self.sameAs) > 0):
            for same in self.sameAs:
                resource(sub,OWL.sameAs,same) 
                
        return sub
class Objects:
    stmt = None
    objects = ""
    startIndex = 0
    endIndex = 0
    isNominal = False
    sameAs = []
    
    def __init__(self,stmt,objDict):
       
        self.stmt = stmt
        self.objects = objDict["entity"]
        if "startIndex" in objDict.keys():
            self.startIndex = objDict["startIndex"]
        else:
            self.startIndex = 0
        if "endIndex" in objDict.keys():
            self.endIndex = objDict["endIndex"]
        else:
            self.endIndex = 0
        
        self.isNominal = objDict["isNominal"]
        self.sameAs = objDict["sameAs"]

    def object_rdf(self): 
        obj = res+""+self.objects.lower()
        resource(self.stmt, RDF.object, obj)
        if self.objects.isdigit():
            resource(obj,RDF.type,RDFS.Literal)
        else:
            resource(obj,RDF.type,RDFS.Resource) # decide on runtime to have a litrel or resource
        
        resource(self.stmt, prop+'objStartIndex', (self.startIndex,XSD.integer),False)
        resource(self.stmt, prop+'objEndIndex', (self.endIndex,XSD.integer),False)
        resource(obj,RDFS.label,(self.objects,XSD.string),False)
        if(self.isNominal):
            resource(obj,prop+'isNominal',(self.isNominal,XSD.boolean),False)
           
        
        if(len(self.sameAs) > 0):
            for same in self.sameAs:
                resource(obj,OWL.sameAs,same) 
                
        
        return obj

class Property:
    stmt = None
    predicate = ''
    isGeneric = False
    equivlent = []
    def __init__(self,stmt,predicate,equivalent,generic):
       
        self.stmt = stmt
        self.predicate = predicate
        self.isGeneric = generic
        self.equivlent = equivalent 
    def property_rdf(self): 
        predicate = reldp+""+u.build_sub_obj(self.predicate)
        resource(self.stmt, RDF.predicate, predicate)
        resource(predicate,RDF.type,RDF.Property)
        resource(predicate,RDFS.label,(self.predicate,XSD.string),False)
        if(self.isGeneric):
            resource(predicate,prop+'isGeneric',(self.isGeneric,XSD.boolean),False)
        if(len(self.equivlent) > 0): 
            for eq in self.equivlent:
                resource(predicate,OWL.equivalentProperty,reldp+""+u.build_sub_obj(eq))#think about that that how to store it
        return predicate
        
class NamedEntity:
    string = None
    ne = []
    sameAs = []
    def __init__(self,string,namedEntities):
        self.string = string
        self.ne = namedEntities
               
    def namedEntity_rdf(self): 
        
        for nentity in self.ne:    
           nentityR = res+""+nentity[0]
           resource(self.string,prop+'hasNamedEntity', nentityR.lower())
           resource(nentityR,RDF.type,PROV.Entity)
           #resource(nentityR,prop+'nerTag',(nentity[1],XSD.string),False)
           resource(nentityR,RDFS.label,(nentity[0],XSD.string),False)
           self.sameAs = u.same_As(nentity[0])
           if(len(self.sameAs) > 0):
               for same in self.sameAs:
                   resource(nentityR, OWL.sameAs, same)

def save_graph(name="test3.ttl", ext = 'ttl' ):
    g.serialize(destination=name, format=ext)

def semEvl(path):
    counter = 0
    stmt_count = 0
    ds = Dataset("SemEval2010", "http://www.kozareva.com/downloads.html", "relation_classification", "sentence", "en").dataset_rdf("01")
    for filename in os.listdir(path):
        if not filename.endswith('.TXT'): continue
        fullname = os.path.join(path, filename)
        
        if filename == "test.TXT":
            dist = 'test'
        elif filename == "train.TXT":
            dist = 'train'
        else:
            dist = 'valid'
        with open(fullname, encoding='utf8') as f:
            equivalent = []
            temp_sent = ""
            pred = ""
            subFobj = False
            meta_data = {}
            for line in tqdm(f):
                if line.startswith('Comment:'):
                    comment = line.split(' ')
                    if len(comment) > 1:    
                        meta_data[RDFS.comment] = str(line.split('Comment:')[1].strip() )
                    else:
                        meta_data = {}
                        continue
                elif u.containsNumber(line[:4]):
                    sent = line.split('\t')[1]
                    subject = sent.split("<e1>")[1].split('</e1>')[0]
                    objects = sent.split("<e2>")[1].split('</e2>')[0]
                elif line == '\n':
                   # ds = objDataset.dataset_rdf("1")
                    sub_entity = u.entity_info(subject, sent,True)
                    obj_entity = u.entity_info(objects, sent,True)#nominal true
                    d_tokens = u.tokens_info(sent)
                    if sent.strip().casefold() != temp_sent.strip().casefold():
                        counter += 1
#                        if counter > 3:
 #                           break
                        temp_sent = sent
                        stmt_count = 0
                        objString = String(dist, "sentence") # will change according to distriubiton and dataset
                        string = objString.string_rdf(counter,ds)
                        Token_Pos_Punct(d_tokens,string).tokens_rdf(counter)
                        statment = Statement(string).statement_rdf(counter,stmt_count,subFobj,meta_data)
                        subject = Subject(statment,sub_entity).subject_rdf()
                        objects = Objects(statment,obj_entity).object_rdf()
                        NamedEntity(string,u.named_entities(sent)).namedEntity_rdf()
                        predicate = Property(statment,pred,equivalent,True).property_rdf()
                    else: 
                        stmt_count += 1
                        statment = Statement(string).statement_rdf(counter,stmt_count,subFobj)
                        subject = Subject(statment,sub_entity).subject_rdf()
                        objects = Objects(statment,obj_entity).object_rdf()
                        predicate = Property(statment,predicate,equivalent,True).property_rdf()
                    
                else:
                    if line.strip() == "Other":
                        pred = "Other"
                    else:
                        first_split = line.split('(')
                        second_split = first_split[1].split(',')[0]
                        pred = first_split[0]
                        if second_split == 'e2':
                            subFobj = True
                        else:
                            subFobj = False
    print(f"Finished with counter = {counter} And Triples = {len(g)}")
                            
                
                
    save_graph(name="17_dumps/semaEval.ttl")
def equRelation(relations_data,dataset,relation):
    equivalent = []
    
    r = relations_data.loc[relations_data[dataset] == relation.strip()]
        
    if r.size > 0:
        for rn in r.iloc[0]:
            if rn == "-":
                continue
            equivalent.append(rn)
    if relation in equivalent:
        equivalent.remove(relation)
    return equivalent
def googleRe(path,relations_data):
    dist = 'train'
    df_list = []
    counter = 132912
    stmt_count = 0
    temp_sent = ""
    equivalent = []
    temp_rel = ""
    subFobj = False 
    ds = Dataset("Google-RE", "https://code.google.com/archive/p/relation-extraction-corpus/", "relation_extraction", "sentence", "en").dataset_rdf("04")

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
        
    for i in tqdm(range(len(data))):
       
        if len(data['sub'][i].split('/')) < 3 or len(data['obj'][i].split('/')) < 3:
            continue
        subject = data['sub'][i].split('/')
        subject = u.id_to_name(subject[2])
        
        objects = u.id_to_name(data['obj'][i].split('/')[2])
        sent = data['evidences'][i][0]['snippet']
        relation = data.pred[i].split('/')
        relation = relation[len(relation) -1]
        if temp_rel != relation:
            equivalent = equRelation(relations_data, "RE-Google-Relation", relation)
        else:
            equivalent = []
        temp_rel = relation
        sub_entity = u.entity_info(subject, sent,False)
        obj_entity = u.entity_info(objects, sent,False)#nominal true
        d_tokens = u.tokens_info(sent)
        subFobj = orderOfEntities(sub_entity,obj_entity)
        
        if sent.strip().casefold() != temp_sent.strip().casefold():
            counter += 1
            temp_sent = sent
            stmt_count = 0
            rdf_builder(True,dist,ds,counter,d_tokens,stmt_count,subFobj,sub_entity,obj_entity,sent,relation,equivalent)
            
        else: 
            stmt_count += 1
            rdf_builder(False,dist,ds,counter,d_tokens,stmt_count,subFobj,sub_entity,obj_entity,sent,relation,equivalent)
            

       # create_RDF(sub_entity,obj_entity,d_tokens,sent,relation,dist,counter,stmt_count,)
    
    save_graph(name="17_dumps/google-re.ttl")
    print(f"Finished with counter = {counter} And Triples = {len(g)}")
def orderOfEntities(sub_entity,obj_entity):
    subFobj = False
    if "startIndex" in sub_entity.keys() and "startIndex" in obj_entity.keys():           
        if sub_entity["startIndex"] < obj_entity["startIndex"]:
            subFobj = False
        else:
            subFobj = True
    return subFobj
    
def rdf_builder(first,dist,ds,counter,d_tokens,stmt_count,subFobj,sub_entity,obj_entity,sent,relation,equivalent,dataset="",numSent="",title=""):
    if dataset == "document":
        objString = String(dist, "document") # will change according to distriubiton and dataset
        string = objString.string_doc_rdf(counter,ds,numSent,title)
    else:
        objString = String(dist, "sentence") # will change according to distriubiton and dataset
        string = objString.string_rdf(counter,ds)
    if first:
        
        Token_Pos_Punct(d_tokens,string).tokens_rdf(counter)
        statment = Statement(string).statement_rdf(counter,stmt_count,subFobj,{})
        subject = Subject(statment,sub_entity).subject_rdf()
        objects = Objects(statment,obj_entity).object_rdf()
        NamedEntity(string,u.named_entities(sent)).namedEntity_rdf()
        predicate = Property(statment,relation,equivalent,False).property_rdf() # explicityly write True when the dataset is Semeval
    else:
        statment = Statement(string).statement_rdf(counter,stmt_count,subFobj,{})
        subject = Subject(statment,sub_entity).subject_rdf()
        objects = Objects(statment,obj_entity).object_rdf()
        predicate = Property(statment,relation,equivalent,False).property_rdf() # explicityly write True when the dataset is Semeval
    

def fewRel(path,relations_data):
    dist = "train"
    counter = 76913
    stmt_count = 0
    temp_sent = ""
    equivalent = []
    temp_rel = ""
    subFobj = False  
    temp_count = 0
    ds = Dataset("FewRel", "http://www.zhuhao.me/fewrel/", "Fewshot_relation_extraction", "sentence", "en").dataset_rdf("03")
    for filename in os.listdir(path):
        if not filename.endswith('.json'): continue
        fullname = os.path.join(path, filename)
        if filename == "test.json":
            dist = 'test'
        elif filename == "train.json":
            dist = 'train'
        else:
            dist = 'valid'
        with open(fullname) as f:
            fewRel_corpus = json.load(f)
            for relation,value in tqdm(fewRel_corpus.items()):
                for row in value:
                    temp_count = temp_count + 1
                    
                    #if temp_count < 757:
                     #   continue
                   # print(temp_count)
                    sub = u.remove_alphaNumeric(row['h'][0].strip())
                    index = row['h'][2]
                    sub_entity = u.entity_info_fewRel(sub, index)
                    obj = u.remove_alphaNumeric(row['t'][0])
                    index = row['t'][2]
                    obj_entity = u.entity_info_fewRel(obj, index)#nominal true
                    sent = ' '.join(map(str, row['tokens']))
                    if temp_rel != relation:
                        equivalent = equRelation(relations_data, "RE-FewRel-Relation", relation)
                    else:
                        equivalent = []
                    temp_rel = relation
                    d_tokens = u.tokens_info(sent)
                    subFobj = orderOfEntities(sub_entity, obj_entity)
                    if sent.strip().casefold() != temp_sent.strip().casefold():
                        counter += 1
                        temp_sent = sent
                        stmt_count = 0
                        rdf_builder(True,dist,ds,counter,d_tokens,stmt_count,subFobj,sub_entity,obj_entity,sent,relation,equivalent)
                        
                    else: 
                        stmt_count += 1
                        rdf_builder(False,dist,ds,counter,d_tokens,stmt_count,subFobj,sub_entity,obj_entity,sent,relation,equivalent)
    save_graph(name="17_dumps/FewRel.ttl")
    print(f"Finished with counter = {counter} And Triples = {len(g)}")

def nytFb(path,relations_data):
    dist = "train"
    counter = 10717
    stmt_count = 0
    temp_sent = ""
    
    temp_rel = ""
    subFobj = False    
    # Will put it's homepage
    ds = Dataset("NYT-FB", "", "distantly_supervised_relation_extraction", "sentence", "en").dataset_rdf("02")
    for filename in os.listdir(path):
        if not filename.endswith('.json'): continue
        fullname = os.path.join(path, filename)
       
        if filename == "test.json":
            dist = 'test'
        elif filename == "train.json":
            dist = 'train'
        else:
            dist = 'valid'
        data = pd.read_json(r''+ fullname, lines=True)
        for i in tqdm(range(len(data))):
            row_relation = data['relationMentions'][i]
            sent = data['sentText'][i]
            d_tokens = u.tokens_info(sent)
#            if i > 2:
 #               break
            for triple in row_relation:
                equivalent = []
                sub = triple['em1Text'].strip()
                obj = triple['em2Text'].strip()
                pred = triple['label'].strip().split('/')
                pred = pred[len(pred) -1]
                if temp_rel != pred:
                    equivalent = equRelation(relations_data, "RE-NYT-Relation", pred)
                else:
                    equivalent = []
                
                temp_rel = pred
                sub_entity = u.entity_info(sub, sent,False)
                obj_entity = u.entity_info(obj, sent,False)#nominal true
                
                subFobj = orderOfEntities(sub_entity, obj_entity)
                if sent.strip().casefold() != temp_sent.strip().casefold():
                    counter += 1
                    
                    temp_sent = sent
                    stmt_count = 0
                    rdf_builder(True,dist,ds,counter,d_tokens,stmt_count,subFobj,sub_entity,obj_entity,sent,pred,equivalent)
                    
                else: 
                    stmt_count += 1 #Correct String variable
                    rdf_builder(False,dist,ds,counter,d_tokens,stmt_count,subFobj,sub_entity,obj_entity,sent,pred,equivalent)
                    

               # create_RDF(sub_entity,obj_entity,d_tokens,sent,relation,dist,counter,stmt_count,)
            
    save_graph(name="17_dumps/nyt-fb.ttl")
    print(f"Finished with counter = {counter} And Triples = {len(g)}")

def webNlg(path,relation_data):
    import xmltodict
    dist = "train"
    counter = 147370
    stmt_count = 0
    temp_sent = ""
    temp_rel = ""
    subFobj = False
    ds = Dataset("WebNLG", "https://webnlg-challenge.loria.fr/", "natural_language_generation", "sentence", "en").dataset_rdf("05")
    for filename in os.listdir(path):
        if not filename.endswith('.xml'): continue
        fullname = os.path.join(path, filename)
        
        x = filename.split("_")
        if 'train' in x :
            dist = 'train'
            
        elif 'dev' in x:
            dist = 'valid'
            
        else:
            dist = 'test'
        
        xml_data = open(fullname,'r').read()  # Read data
        xmlDict = xmltodict.parse(xml_data)  # Parse XML
        for i in tqdm(xmlDict['benchmark']['entries']['entry']):
            
            rel = i['modifiedtripleset']['mtriple']#.split('|')
            sentence = []
            if(type(i['lex']) == list):
                for c in range(len(i['lex'])):
                    sent = i['lex'][c]['#text']
                    sentence.append(sent)
                sent = sentence[u.get_max_str_index(sentence)]
            else:
                sent = i['lex']['#text']
            d_tokens = u.tokens_info(sent)
            if type(rel) != list:
                rel = [rel]
            for triple in rel:    
                equivalent = []
                
                val = triple.split('|')
                
                sub = u.remove_alphaNumeric(val[0].strip())
                
                obj = u.remove_alphaNumeric(val[2].strip())
                pred = u.remove_alphaNumeric(val[1].strip())
                if temp_rel != pred:
                    equivalent = equRelation(relation_data, "RE-WebNLG-Relation", pred)
                else:
                    equivalent = []
                temp_rel = pred
                
                sub_entity = u.entity_info(sub, sent,False)
                obj_entity = u.entity_info(obj, sent,False)#nominal true
                
                subFobj = orderOfEntities(sub_entity, obj_entity)
                if sent.strip().casefold() != temp_sent.strip().casefold():
                    counter += 1
                    temp_sent = sent
                    stmt_count = 0
                    rdf_builder(True,dist,ds,counter,d_tokens,stmt_count,subFobj,sub_entity,obj_entity,sent,pred,equivalent)
                    
                else: 
                    stmt_count += 1 #Correct String variable
                    rdf_builder(False,dist,ds,counter,d_tokens,stmt_count,subFobj,sub_entity,obj_entity,sent,pred,equivalent)
                    

               # create_RDF(sub_entity,obj_entity,d_tokens,sent,relation,dist,counter,stmt_count,)
   
    save_graph(name="17_dumps/webNlg.ttl")
    print(f"Finished with counter = {counter} And Triples = {len(g)}")
def wikiRe(path,relation_data):
    counter = 157934
    stmt_count = 0
    temp_sent = ""
    temp_rel = ""
    subFobj = False
    
    ds = Dataset("WikipediaWikidata", "https://tudatalib.ulb.tu-darmstadt.de/handle/tudatalib/2776", "Distant_Supervision_relation_extraction", "sentence", "en").dataset_rdf("06")
    dist = 'train'
    for filename in os.listdir(path):
        if not filename.endswith('.json'): continue
        fullname = os.path.join(path, filename)
        if filename == "test.json":
            dist = 'test'
        elif filename == "training.json":
            dist = 'train'
        else:
            dist = 'valid'
        with open(fullname) as f:
            wikidata_corpus = json.load(f)
            for i in tqdm(range(len(wikidata_corpus))):
                entities = {}
                equivalent = []
                
                sent = ' '.join(map(str, wikidata_corpus[i]['tokens']))
                d_tokens = u.tokens_info_wikiRe(wikidata_corpus[i]['tokens'],sent)
                for entry in wikidata_corpus[i]['vertexSet']:
                    entities[entry['lexicalInput']] = entry['tokenpositions']
                for r_entry in wikidata_corpus[i]['edgeSet']:
                    for ent_id , ent in entities.items():
                        if ent == r_entry['left']:
                            
                            sub_entity = u.entity_info_fewRel(ent_id, ent,False,sentence=sent)
                        elif ent == r_entry['right']:
                            
                            obj_entity = u.entity_info_fewRel(ent_id, ent,False,sentence=sent)
                        else:
                            continue
                    pred = r_entry['kbID']
                    if temp_rel != pred:
                        equivalent = equRelation(relation_data, "RE-WikiRE-Relation", pred)
                    else:
                        equivalent = []
                    temp_rel = pred
                    subFobj = orderOfEntities(sub_entity, obj_entity)
                    if sent.strip().casefold() != temp_sent.strip().casefold():
                        counter += 1
                        temp_sent = sent
                        stmt_count = 0
                        rdf_builder(True,dist,ds,counter,d_tokens,stmt_count,subFobj,sub_entity,obj_entity,sent,pred,equivalent)
                        
                    else: 
                        stmt_count += 1 #Correct String variable
                        rdf_builder(False,dist,ds,counter,d_tokens,stmt_count,subFobj,sub_entity,obj_entity,sent,pred,equivalent)
                        

                   # create_RDF(sub_entity,obj_entity,d_tokens,sent,relation,dist,counter,stmt_count,)
    
    save_graph(name="17_dumps/wikiRe.ttl")
    print(f"Finished with counter = {counter} And Triples = {len(g)}")
                           
def docRed(path,relation_data):
    counter = 1014151
    stmt_count = 0
    temp_sent = ""
    temp_rel = ""
    subFobj = False
    
    ds = Dataset("DocRed", "https://github.com/thunlp/DocRED", "document_level_relation_extraction", "document", "en").dataset_rdf("07")
    dist = 'train'
    for filename in os.listdir(path):
        if not filename.endswith('.json'): continue
        fullname = os.path.join(path, filename)
        if filename == "test.json":
            dist = 'test'
        elif filename == "train.json":
            dist = 'train'
        else:
            dist = 'valid'
        with open(fullname) as f:
            docred_corpus = json.load(f)
            for entry in tqdm(docred_corpus):
                vertexSet = entry['vertexSet']
                title = entry['title']
                labels = entry['labels']
                
                sent = ""
                num_sent = len(entry['sents'])
                sent_tok = []
                for x in entry['sents'] :
                    for i in x:
                        sent_tok.append(i)
                for s in entry['sents']:
                    
                    sent += ' '.join([str(item) for item in s])
                    sent += " "
                d_tokens = u.tokens_info_wikiRe(sent_tok, sent)
                for triple in labels:
                    equivalent = []
                    pred = triple['r']
                    sub_pos = triple['h']
                    obj_pos = triple['t']
                    sub = u.remove_alphaNumeric(vertexSet[sub_pos][0]['name'])
                    obj = u.remove_alphaNumeric(vertexSet[obj_pos][0]['name'])
                    sub_entity = u.entity_info(sub,sent)
                    obj_entity = u.entity_info(obj, sent)
                    if temp_rel != pred:
                        equivalent = equRelation(relation_data, "WikidataIds", pred)
                    else:
                        equivalent = []
                    subFobj = orderOfEntities(sub_entity, obj_entity)
                    if sent.strip().casefold() != temp_sent.strip().casefold():
                        counter += 1
                        temp_sent = sent
                        stmt_count = 0
                        rdf_builder(True,dist,ds,counter,d_tokens,stmt_count,subFobj,sub_entity,obj_entity,sent,pred,equivalent,"document",num_sent,title)
                        
                    else: 
                        stmt_count += 1 #Correct String variable
                        rdf_builder(False,dist,ds,counter,d_tokens,stmt_count,subFobj,sub_entity,obj_entity,sent,pred,equivalent,"document",num_sent,title)
    
    save_graph(name="17_dumps/docRed.ttl")
    print(f"Finished with counter = {counter} And Triples = {len(g)}")            
   
def create_graph():
    g = Graph()
    prop = Namespace("http://reld.dice-research.org/schema/")
    res = Namespace("http://reld.dice-research.org/resource/")
    #datasetURI = Namespace("https://reld.dice-research.org/")
    dbo = Namespace("http://dbpedia.org/ontology/")
    freebase = Namespace("http://rdf.freebase.com/ns")
    wikidata = Namespace("http://www.wikidata.org/prop/statement/")
    owl = Namespace("http://www.w3.org/2002/07/owl#")
    dc = Namespace("http://purl.org/dc/elements/1.1/")
    dcterms = Namespace("http://purl.org/dc/terms/")
    nif = Namespace("http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#")
    prov = Namespace("http://www.w3.org/ns/prov#")
    dbpedia = Namespace("http://dbpedia.org/property/")
    rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")

    g.bind("reld", prop)
    g.bind("reldr", res)
    g.bind("dcterms",dcterms)
    g.bind("dbo",dbo)
    g.bind("ps",wikidata)
    g.bind('freebase',freebase)
    g.bind('owl',owl)
    g.bind('dbo',dbpedia)
    g.bind('rdf',rdf)
    g.bind('prov',prov)
    g.bind('dc',dc)
    g.bind('nif',nif)


    return g
def trexRe(path,relation_data):
    counter = 1018164
    stmt_count = 0
    temp_sent = ""
    temp_rel = ""
    subFobj = False
    allStat = 0
    all_triple = 0
    
    ds = Dataset("T-REx", "https://hadyelsahar.github.io/t-rex/downloads/", "relation_extraction_and_natural_language", "document", "en").dataset_rdf("08")
    global g
    for filename in tqdm(os.listdir(path)):
        if not filename.endswith('.json'): continue
        fullname = os.path.join(path, filename)
        name = str(filename)+"-"+str(counter)+".ttl"
        
        g.serialize(destination="07_trex_dumps/"+name, format = "ttl")
        print(f"File {name} is saved with {len(g)} Triples")
        
        g = create_graph()
        
        if filename == "test.json":
           dist = 'test'
        elif filename == "valid.json":
           dist = 'valid'
        else:
            dist = 'train'
        data = pd.read_json(r''+ fullname, lines=True)
        data = data.T
        print(fullname)
        for i in tqdm(range(len(data))):
            sent = data[0][i]['text']
            title = data[0][i]['title']
            row_relation = data[0][i]['triples']
            d_tokens = u.tokens_info(sent)
            num_sent = len(data[0][i]['sentences_boundaries'])
            for triple in row_relation:
                equivalent = []
                pred = triple['predicate']['uri'].split('/')[-1]
                sub = u.remove_alphaNumeric(triple['subject']['surfaceform'])
                obj = u.remove_alphaNumeric(triple['object']['surfaceform'])
                
                sub_entity = u.entity_info(sub,sent)
                obj_entity = u.entity_info(obj, sent)
                if sub == "XMLSchema#dateTime":
                    sub = triple['subject']['surfaceform']
                if obj == "XMLSchema#dateTime":
                    obj = triple['object']['surfaceform']
                if temp_rel != pred:
                    equivalent = equRelation(relation_data, "WikidataIds", pred)
                else:
                    equivalent = []
                subFobj = orderOfEntities(sub_entity, obj_entity)
                if sent.strip().casefold() != temp_sent.strip().casefold():
                    counter += 1
                    temp_sent = sent
                    stmt_count = 0
                    allStat += stmt_count
                    rdf_builder(True,dist,ds,counter,d_tokens,stmt_count,subFobj,sub_entity,obj_entity,sent,pred,equivalent,"document",num_sent,title)
                    
                else: 
                    stmt_count += 1 #Correct String variable
                    rdf_builder(False,dist,ds,counter,d_tokens,stmt_count,subFobj,sub_entity,obj_entity,sent,pred,equivalent,"document",num_sent,title)
                
            
            
        all_triple +=  len(g)
    save_graph(name="T-REx.ttl")
    print(f"Finished with counter = {counter} And Triples = {all_triple} and staments = {allStat}")            
               
                
    
    
def main():
    list_dataset = ["DocRed"]#["WebNLG", "Google-RE", "NYT-FB", "FewRel", "SemEval2010" ,"Wiki-RE","Trex"]
    relation = pd.read_csv('data/AllRelationWithCrossCheck.csv')
    relation = relation.drop(['Wrid','Nrid','Wgrid','Frid','Srid','Grid','Drid'],axis=1)
    relation.fillna('-', inplace = True)
    for x in list_dataset:
       
        if x == "SemEval2010":
            semEvl('data/SemEval/')
            #remove_graph(g)
        elif x == "Google-RE":
            googleRe('data/google',relation)
        elif x == "FewRel":
            fewRel('data/fewrel',relation)
        elif x == "NYT-FB":
            nytFb('data/nyt',relation)
        elif x == "WebNLG":
            webNlg('data/WebNLG',relation)
        elif x == "Wiki-RE":
            wikiRe('data/wikiRe',relation)
        elif x == "DocRed":
            docRed("data/docred",relation)
        elif x == "Trex":
            trexRe("data/trex",relation)
        elif x == 'unknown':
            ds = Dataset("T-REx", "https://hadyelsahar.github.io/t-rex/downloads/", "relation_extraction_and_natural_language", "document", "en").dataset_rdf("unknown")
            st = String('valid', 'sentence').string_rdf(1,ds)
            dictT = {'pos':['Por','nam','v','N'],'tokens':['Por','nam','v','N'],'punct':['Por','nam','v','N']}
            tokenId = Token_Pos_Punct(dictT, st).tokens_rdf(1)
            stment = Statement(st).statement_rdf(1, 1, False)
            objetDict = {'entity':'3343','startIndex':3,'endIndex':6,'isNominal':False,'sameAs':[]}
            sub = Subject(stment, objetDict).subject_rdf()
            obj = Objects(stment,objetDict).object_rdf()
            proerty = Property(stment, "birth Place", ['birthPlace','P12'], True).property_rdf()
            ne = NamedEntity(st, ('barack hussain','Per')).namedEntity_rdf()
            save_graph(name="unknown.ttl")
if __name__ == "__main__":
    main()


