import sqlite3
import config
import cPickle as pickle
import re

remove_specific_re=re.compile(r'#\w+|@\w|https?://[\w/_.-]+',re.UNICODE)
space_re=re.compile(r'\s+',re.UNICODE)

def min_no_tweets():
  print 'Performing min_no_tweets by user'
  conn=sqlite3.connect(config.DB)
  c=conn.cursor()
  users={}
  c.execute('SELECT user FROM tweets')
  for user in c.fetchall():
    user=user[0]
    users[user]=users.get(user,0)+1
  all_users=users.keys()
  for user in all_users:
    if users[user]<config.MIN_NO_TWEETS:
      del users[user]
  print 'Users:',len(users),'/',len(all_users)
  return set(users)

def user_langid(candidate):
  print 'Performing langid by user'
  conn=sqlite3.connect(config.DB)
  c=conn.cursor()
  users=set()
  user_text={}
  from langid import classify
  c.execute('SELECT user,tweet FROM tweets')
  count=0
  for user,status in c.fetchall():
    count+=1
    if count%100000==0:
      print 'Processed:',count
    if user not in candidate:
      continue
    status=pickle.loads(str(status))
    if user not in user_text:
      user_text[user]=[]
    user_text[user].append(space_re.sub(' ',remove_specific_re.sub(' ',status.text)).strip())
  count=0
  lang_distr={}
  for user in user_text:
    count+=1
    if count%1000==0:
      print 'Users:',count,'/',len(user_text)
    lang=classify(' '.join(user_text[user]))[0]
    if lang in config.LANGS:
      users.add(user)
    lang_distr[lang]=lang_distr.get(lang,0)+1
  print len(users)
  print sorted(lang_distr.items(),key=lambda x:-x[1])
  conn.close()
  print 'Users:',len(users),'/',len(user_text)
  return users

def user_country(candidate):
  print 'Performing country by user'
  import reverse_geocoder as rg
  conn=sqlite3.connect(config.DB)
  c=conn.cursor()
  users=set()
  from langid import classify
  c.execute('SELECT user,tweet FROM tweets')
  count=0
  #user_coordinates=[]
  user_countries={}
  for user,status in c.fetchall():
    count+=1
    if count%100000==0:
      print 'Processed:',count
    if user not in candidate:
      continue
    status=pickle.loads(str(status))
    if status.place==None:
      continue
    country=status.place.country_code
    #lon,lat=status.geo['coordinates']
    if user not in user_countries:
      user_countries[user]=[0,0]
    user_countries[user][1]+=1
    if country in config.COUNTRIES:
      user_countries[user][0]+=1
    #user_coordinates.append((user,(lon,lat)))
  print 'Processed:',count
  #countries=[e['cc'] for e in rg.search([e[1] for e in user_coordinates])]
  #for (user, lonlat),country in zip(user_coordinates,countries):
  #  user_countries[user][1]+=1
  #  if country in config.COUNTRIES:
  #    user_countries[user][0]+=1
  for user in user_countries:
    #print user,user_countries[user]
    if user_countries[user][0]>=user_countries[user][1]/2.:
      users.add(user)
  conn.close()
  print 'Users:',len(users),'/',len(user_countries)
  return users

if __name__=='__main__':
  users=min_no_tweets()
  langid=user_langid(users)
  country=user_country(users)
  users=langid.intersection(country)
  print 'Saving users:',len(users)
  pickle.dump(users,open('users.pickle','w'),1)
