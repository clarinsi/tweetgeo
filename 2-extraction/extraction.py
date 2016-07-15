#-*-coding:utf8-*-
import sqlite3
import cPickle as pickle
import csv
import re
from langid import classify
import sys
import config

def metadata(status,argument,function=lambda x:x):
  if function==None:
    function=lambda x:x
  return function(eval('status.'+argument))

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

def regex_choice(text,regex_pairs):
  found=set()
  for regex,value in regex_pairs:
    if regex.search(text)!=None:
      found.add(value)
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
    for argument in ('id_str','user.screen_name','geo[\'coordinates\'][1]','geo[\'coordinates\'][0]','text'):
      entry.append(normalise_space(metadata(status,argument)))
    for (argument,function) in config.EXTRACTION_STATUS:
      entry.append(normalise_space(metadata(status,argument,function)))
    for function,args in config.EXTRACTION_TEXT:
      entry.append(normalise_space(function(text,*args)))
    text=status.text.lower()
    for function,args in config.EXTRACTION_LOWER:
      entry.append(normalise_space(function(text,*args)))
    text=config.normalise(status.text)
    for function,args in config.EXTRACTION_NORMALISED:
      entry.append(normalise_space(function(text,*args)))
    out.write('\t'.join(entry).encode('utf8')+'\n')
  out.close()
