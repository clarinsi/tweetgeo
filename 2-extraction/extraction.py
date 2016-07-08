#-*-coding:utf8-*-
import sqlite3
import cPickle as pickle
import csv
import re
from langid import classify
import sys
import config

def tidf(status):
  return status.id_str

def userf(status):
  return status.user.screen_name

def lonf(status):
  return str(status.geo['coordinates'][1])

def latf(status):
  return str(status.geo['coordinates'][0])

def textf(status):
  return status.text

def langf(status):
  return status.lang

def regex_choice(text,regex_dict):
  found=set()
  for k in regex_dict:
    if regex_dict[k].search(text)!=None:
      found.add(k)
  if len(found)==1:
    return list(found)[0]
  else:
    return 'NA'

def lexicon_choice(text,resource):
  value='NA'
  for token in config.tokenize(text):
    if token in resource:
      if value=='NA':
        value=resource[token]
      else:
        if value!=resource[token]:
          return 'NA'
  return value

def load_resource(path):
  resource=[]
  for line in open(path):
    resource.append(line.strip().decode('utf8').split('\t'))
  return dict(resource)

space_re=re.compile(r'\s+',re.UNICODE)

def normalise_space(text):
  return space_re.sub(' ',text,re.UNICODE).strip()

if __name__=='__main__':
  try:
    users=pickle.load(open('users.pickle'))
  except:
    users=None
  conn=sqlite3.connect(config.DB)
  c=conn.cursor()
  c.execute('SELECT user,tweet FROM tweets')
  out=open(config.TSV,'w')
  counter=0
  for user,status in c.fetchall():
    counter+=1
    if counter%100000==0:
      print 'Processed:',counter
      sys.stdout.flush()
    if users!=None:
      if user not in users:
        continue
    status=pickle.loads(str(status))
    if status.geo==None:
      continue
    entry=[]
    for function in (tidf,userf,lonf,latf,textf):
      entry.append(normalise_space(function(status)))
    for function in config.EXTRACTION_STATUS:
      entry.append(normalise_space(function(status)))
    text=status.text.lower()
    for function,args in config.EXTRACTION_TEXT:
      entry.append(normalise_space(function(text,*args)))
    text=config.normalise(status.text)
    for function,args in config.EXTRACTION_NORMALISED:
      entry.append(normalise_space(function(text,*args)))
    out.write('\t'.join(entry).encode('utf8')+'\n')
  out.close()
