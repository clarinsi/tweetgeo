import sqlite3
import config
import cPickle as pickle
import csv

def tid(status):
  return status.id_str

def user(status):
  return status.user.screen_name.encode('utf8')

def lon(status):
  return str(status.geo['coordinates'][0])

def lat(status):
  return str(status.geo['coordinates'][1])

def text(status):
  return status.text.encode('utf8')

def lang(status):
  return status.lang.encode('utf8')

if __name__=='__main__':
  conn=sqlite3.connect(config.DB)
  c=conn.cursor()
  c.execute('SELECT tweet FROM tweets WHERE filter=0')
  out=csv.writer(open(config.TSV,'w'), delimiter='\t', quotechar='"')
  for status in c.fetchall():
    status=pickle.loads(str(status[0]))
    entry=[]
    for function in (tid,user,lon,lat,text):
      entry.append(function(status))
    for function in config.EXTRACTION:
      function=eval(function)
      entry.append(function(status))
    out.writerow(entry)
