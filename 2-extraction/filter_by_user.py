import sqlite3
import config
import cPickle as pickle
import csv
import re

remove_specific_re=re.compile(r'#\w+|@\w|https?://[\w/_.-]+',re.UNICODE)
space_re=re.compile(r'\s+',re.UNICODE)

def user_langid(langs):
  try:
    users=pickle.load(open('users.pickle'))
  except:
    users=set()
  user_text={}
  from langid import classify
  c.execute('SELECT user,tweet FROM tweets')
  count=0
  for user,status in c.fetchall():
    count+=1
    status=pickle.loads(str(status))
    if user not in user_text:
      user_text[user]=[]
    user_text[user].append(space_re.sub(' ',remove_specific_re.sub(' ',status.text)).strip())
    if count%100000==0:
      print 'Processed:',count
  count=0
  lang_distr={}
  for user in user_text:
    count+=1
    if count%1000==0:
      print 'Users:',count,'/',len(user_text)
    """
    lang_distr={}
    for i in range(len(user_text[user])/10+1):
      lang=classify(' '.join(user_text[user][i*10:(i+1)*10]))[0]
      lang_distr[lang]=lang_distr.get(lang,0)+1
    ours=0
    for lang in lang_distr:
      if lang in langs:
        ours+=lang_distr[lang]
    if ours*2>=sum(lang_distr.values()):
      users.add(user)
    """
    lang=classify(' '.join(user_text[user]))[0]
    if lang in langs:
      users.add(user)
    lang_distr[lang]=lang_distr.get(lang,0)+1
  print len(users)
  print sorted(lang_distr.items(),key=lambda x:-x[1])
  pickle.dump(users,open('users.pickle','w'),1)

if __name__=='__main__':
  conn=sqlite3.connect(config.DB)
  c=conn.cursor()
  user_langid(config.LANG)
  conn.close()