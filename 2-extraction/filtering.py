import sqlite3
import config
import cPickle as pickle
import csv

langs=['pt','es','cat']

if __name__=='__main__':
  conn=sqlite3.connect(config.DB)
  c=conn.cursor()
  c.execute('UPDATE tweets SET filter=0')
  #c.execute('UPDATE tweets SET filter=1 WHERE lang NOT IN (%s)' % ','.join('?'*len(langs)),langs)
  conn.commit()