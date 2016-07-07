import sqlite3
import config
import cPickle as pickle
import csv

def user_langid(langs):
  try:
    users=pickle.load(open('users.pickle'))
  except:
    users=set()
  from langid import classify
  c.execute('SELECT user,GROUP_CONCAT(text," ") FROM tweets GROUP BY user')
  count=0
  for user,text in c.fetchall():
    count+=1
    lang=classify(text)[0]
    if lang in langs:
      users.add(user)
    if count%10==0:
      print count
  pickle.dump(users,open('users.pickle','w'),1)

if __name__=='__main__':
  conn=sqlite3.connect(config.DB)
  c=conn.cursor()
  user_langid(['hr','sr','bs'])
