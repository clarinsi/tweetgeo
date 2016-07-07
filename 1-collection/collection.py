#!/usr/bin/python
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
import cPickle as pickle
from datetime import datetime
from httplib import IncompleteRead
import sys
from time import sleep
import sqlite3
import config
import os

class StdOutListener(StreamListener):

  def __init__(self,cursor,connection,log):
    super(StdOutListener, self).__init__()
    self.e420=60
    self.cursor=cursor
    self.connection=connection
    self.old_entries=cursor.execute('SELECT COUNT(*) FROM tweets').fetchone()[0]
    self.new_entries=0
    self.log=log

  def on_status(self, status):
    self.e420=60
    added=False
    if status.coordinates!=None:
      self.cursor.execute('INSERT OR IGNORE INTO tweets VALUES(?,?,?,?)',(status.id_str,status.user.screen_name,status.lang,buffer(pickle.dumps(status,2))))
      self.connection.commit()
      self.new_entries+=1
      self.log.write(datetime.now().isoformat()+' New entries: '+str(self.new_entries)+' All entries: '+str(self.new_entries+self.old_entries)+'\n')
    self.log.flush()
 
  def on_error(self, status):
    if status==420:
      self.log.write(datetime.now().isoformat()+' ERROR 420, sleeping '+str(self.e420)+'\n')
      sleep(self.e420)
      self.e420*=2
    else:
      self.log.write(datetime.now().isoformat()+' ERROR '+str(status)+', sleeping 5\n')
      sleep(5)
    self.log.flush()

if __name__=='__main__':
  import config
  log=open(config.PROJECT+'.log','a')
  db_path=config.PROJECT+'.db'
  existing_db=os.path.isfile(db_path)
  conn=sqlite3.connect(config.PROJECT+'.db')
  c=conn.cursor()
  if not existing_db:
    c.execute('CREATE TABLE tweets (tid text primary key, user text, lang text, tweet blob)')
    conn.commit()
    log.write(datetime.now().isoformat()+' New database, table created.\n')
  else:
    log.write(datetime.now().isoformat()+' Old database.\n')
  l=StdOutListener(c,conn,log)
  log.flush()
  auth=OAuthHandler(config.CONSUMER_KEY,config.CONSUMER_SECRET)
  auth.set_access_token(config.ACCESS_TOKEN,config.ACCESS_TOKEN_SECRET)
  while True:
    try:
      stream=Stream(auth,l)
      stream.filter(locations=[config.MINLON,config.MINLAT,config.MAXLON,config.MAXLAT])
    except:
      log.write(str(sys.exc_info())+'\n')
      log.write(datetime.now().isoformat()+' sleeping 0 and restarting\n')
      continue
