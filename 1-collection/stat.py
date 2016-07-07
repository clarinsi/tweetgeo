#!/usr/bin/python
import sqlite3
import config
if __name__=='__main__':
  conn=sqlite3.connect(config.PROJECT+'.db')
  cursor=conn.cursor()
  print 'Entries:',cursor.execute('SELECT COUNT(*) FROM tweets').fetchone()[0]
  print 'Users:',cursor.execute('SELECT COUNT(DISTINCT user) FROM tweets').fetchone()[0]
  print 'Top users:',cursor.execute('SELECT user,COUNT(user) as count FROM tweets GROUP BY user ORDER BY count DESC LIMIT 10').fetchall()
  cursor.execute('SELECT lang,COUNT(lang) AS count FROM tweets GROUP BY lang ORDER BY count DESC')
  print 'Langs:',cursor.fetchall()
  conn.close()  