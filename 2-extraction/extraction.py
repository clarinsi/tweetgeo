#-*-coding:utf8-*-
import sqlite3
import cPickle as pickle
import csv
import re
from langid import classify
import sys

def tidf(status):
  return status.id_str

def userf(status):
  return status.user.screen_name.encode('utf8')

def lonf(status):
  return str(status.geo['coordinates'][1])

def latf(status):
  return str(status.geo['coordinates'][0])

def textf(status):
  return status.text.encode('utf8')

def langf(status):
  return status.lang.encode('utf8')

dia={u'č':u'c',u'š':u's',u'ž':u'z',u'ć':u'c',u'đ':u'd',u'Č':u'C',u'Š':u'S',u'Ž':u'Z',u'Ć':u'C',u'Đ':u'D'}

def remove_diacritics(text):
  result=''
  for char in text:
    result+=dia.get(char,char)
  return result

repetition_re=re.compile(r'(.)\1+')
space_re=re.compile(r'\s+',re.UNICODE)

def normalise(text):
  return remove_diacritics(repetition_re.sub(r'\1',space_re.sub(' ',text.lower())))

def contains(text,regex):
  if regex.search(status.text)!=None:
    return 'yes'
  else:
    return 'no'

token_re=re.compile(r'#\w+|@\w|https?://[\w/_.-]+|\w+',re.UNICODE)

def tokenize(text):
  return token_re.findall(text)

def load_resource(path):
  resource=[]
  for line in open(path):
    resource.append(line[:-1].decode('utf8').split('\t'))
  return dict(resource)

def apply_token_resource(text,path):
  value='NA'
  resource=load_resource(path)
  for token in tokenize(text):
    if token in resource:
      if value=='NA':
        value=resource[token]
      else:
        if value!=resource[token]:
          return 'NA'
  return value

if __name__=='__main__':
  try:
    users=pickle.load(open('users.pickle'))
  except:
    users=None
  #print normalise(u'jučččččerrrrr g     g')
  #print apply_token_resource('smijesan je lepo','resources/yat')
  #sys.exit()
  import config
  conn=sqlite3.connect(config.DB)
  c=conn.cursor()
  c.execute('SELECT user,tweet FROM tweets')
  out=csv.writer(open(config.TSV,'w'), delimiter='\t', quotechar='"')
  counter=0
  for user,status in c.fetchall():
    counter+=1
    if users!=None:
      if user not in users:
        #print 'dismissing',user
        continue
      #print user
    status=pickle.loads(str(status))
    if status.geo==None:
      continue
    #else:
    #  print status.geo
    entry=[]
    for function in (tidf,userf,lonf,latf,textf):
      entry.append(function(status))
    for function in config.EXTRACTION_STATUS:
      entry.append(function(status))
    text=status.text.lower()
    for function,args in config.EXTRACTION_TEXT:
      entry.append(function(text,*args))
    text=normalise(status.text)
    for function,args in config.EXTRACTION_NORMALISED:
      entry.append(function(text,*args))
    out.writerow(entry)
    if counter%1000==0:
      print counter
