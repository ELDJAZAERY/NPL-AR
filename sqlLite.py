# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 23:27:49 2018

@author: ELDJAZAERY
"""

 
import sqlite3
from sqlite3 import Error
 
 
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None
 
 
def select_ALL(conn):
    cur = conn.cursor()
    cur.execute("select word , root , meaning from WordsTable")
 
    rows = cur.fetchall()
 
    for row in rows:
        print(row)
 
def select(conn,word):
    cur = conn.cursor()    
    request = '''
        SELECT WT.word, WT.root, WT.meaning
            FROM WordsTable AS WT, Keys AS K
            WHERE  WT.word = K.wordkey
    				AND
    			     K.searchwordkey = "'''+word+'''"
        '''

    cur.execute(request)
    rows = cur.fetchall()
    
    
    for row in rows:
        print("\n")
        for att in row:
            for r in att.split("|"):
                print(r);
        
 
import os 
def main():
    base_path = os.path.dirname(os.path.realpath(__file__))
    db_file = os.path.join(base_path, "apk\AlmaanyArArFinal_NEW.db")
    conn = create_connection(db_file);
    word = "اكل"
    select(conn,word)


main()



    