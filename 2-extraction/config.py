#-*-coding:utf8-*-
from extraction import *

# languages used by user_langid in filter_by_user.py
LANG=['hr','sr','bs']

DB='../1-collection/hbs-twitter.db'

TSV='hbs-twitter.tsv'

import os
RESOURCES={}
for file in os.listdir('resources'):
  RESOURCES[file]=load_resource('resources/'+file)

dia={u'č':u'c',u'š':u's',u'ž':u'z',u'ć':u'c',u'đ':u'dj'}

def remove_diacritics(text):
  result=''
  for char in text:
    result+=dia.get(char,char)
  return result

repetition_re=re.compile(r'(.)\1+')
space_re=re.compile(r'\s+',re.UNICODE)

def normalise(text):
  return remove_diacritics(repetition_re.sub(r'\1',space_re.sub(' ',text.lower(),re.UNICODE)))

token_re=re.compile(r'#\w+|@\w|https?://[\w/_.-]+|\w+',re.UNICODE)

def tokenize(text):
  return token_re.findall(text)

# pairs of arguments from Status objects to be extracted and functions to be applied, None for lambda x:x
EXTRACTION_STATUS=[('lang',None),]
# pairs of function names and arguments / resources
EXTRACTION_TEXT=[]
# same as previous, but to be run on lowercased text
EXTRACTION_LOWER=[(lexicon_choice,(RESOURCES['stosta'],)),(regex_choice,([(re.compile(r'\b(da li)\b',re.UNICODE),'dali'),(re.compile(r'\b(je li)\b',re.UNICODE),'jeli')],))]
# same as before, but to be run on normalised text
EXTRACTION_NORMALISED=[]
EXTRACTION_NORMALISED=[(lexicon_choice,(RESOURCES['yat'],)),(lexicon_choice,(RESOURCES['prijateljdrug'],)),(lexicon_choice,(RESOURCES['rdrop'],)),(lexicon_choice,(RESOURCES['breba'],)),(lexicon_choice,(RESOURCES['months'],)),(lexicon_choice,(RESOURCES['mnogo'],)),(regex_choice,([(re.compile(r'^i\'m at '),'noise'),(re.compile(ur'по курсу'),'noise')],))]
