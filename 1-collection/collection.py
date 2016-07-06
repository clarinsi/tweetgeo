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

def load_emojis():
  import re
  emoji_re=re.compile(r"<td class='chars'>(.+?)</td>")
  emojis=emoji_re.findall(open('full-emoji-list.html').read().decode('utf8'))
  return emojis

def contains_emojis(tweet):
  for index in range(len(tweet)):
    if index+1<len(tweet):
      if tweet[index:index+1] in emojiset:
        return True
    if tweet[index] in emojiset:
      return True
  return False

current=datetime.now().strftime('%Y-%m-%d')
try:
  statuses=pickle.load(open('statuses_'+current))
  print 'old statuses',len(statuses)
except:
  statuses=[]
"""
try:
  statuses_all=pickle.load(open('statuses_all_'+current))
  print 'old all statuses',len(statuses_all)
except:
  statuses_all=[]
"""

class StdOutListener(StreamListener):

  def __init__(self, api=None):
    super(StdOutListener, self).__init__()
    self.e420=60

  def on_status(self, status):
    self.e420=60
    added=False
    global statuses
    """
    global statuses_all
    """
    global current
    if status.coordinates!=None:
      if contains_emojis(status.text):
        #print status.coordinates
        #print status.place
        stat['has']+=1
        statuses.append(status)
        added=True
      else:
        stat['not']+=1
      """
      statuses_all.append(status)
      """
    if sum(stat.values())%500==0:
      print datetime.now().isoformat(),stat.items(),len(statuses)#,len(statuses_all)
    if len(statuses)%5000==0:
      if added:
        date=datetime.now().strftime('%Y-%m-%d')
        pickle.dump(statuses,open('statuses_'+current,'w'),1)
        """
        pickle.dump(statuses_all,open('statuses_all_'+current,'w'),1)
        """
        print datetime.now().isoformat(),'writing down',len(statuses)#,len(statuses_all)
        if date!=current:
          statuses=[]
          #statuses_all=[]
          current=date
        added=False
    sys.stdout.flush()
    #print status.text,status.coordinates,dir(status)
 
  def on_error(self, status):
    if status==420:
      print datetime.now().isoformat(),'ERROR',status,'sleeping',self.e420
      sleep(self.e420)
      self.e420*=2
    else:
      print datetime.now().isoformat(),'ERROR',status,'sleeping 5'
      sleep(5)
    sys.stdout.flush()

if __name__=='__main__':
  CONSUMER_KEY='sZvIU3JWlneMxR2FRCnmSr1uP'
  CONSUMER_SECRET='VteqZChXKuDo7h8RjzQQp7zTLJzH5fX5PZjVOwwXILilS8c9wg'
  ACCESS_TOKEN='194186221-ssZQZcOKWPuXu9bqHRh5JK3IdfxEwXfHKle5r2kw'
  ACCESS_TOKEN_SECRET='xtehbyYyf6wsQBtrgX1qKqhTg3FsQH9PyPBEdcr86drkt'
  emojis=load_emojis()
  emojiset=set(emojis)
  stat={'has':0,'not':0}
  l=StdOutListener()
  auth=OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
  auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
  while True:
    try:
      stream=Stream(auth,l)
      stream.filter(locations=[-180,-90,180,90])
    except:
      print sys.exc_info()
      print datetime.now().isoformat(),'sleeping 0 and restarting'
      #sleep(5)
      continue
  #stream.filter(track=emojis[:100])
