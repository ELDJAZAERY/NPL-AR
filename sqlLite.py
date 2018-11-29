# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 23:27:49 2018

@author: ELDJAZAERY
"""

 
import sqlite3
from sqlite3 import Error
import os 
 


### Create Connection with SQL LITE DB ####
 
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


base_path = os.path.dirname(os.path.realpath(__file__))
db_file = os.path.join(base_path, "db\AlmaanyArArFinal_NEW.db")
conn = create_connection(db_file);
 
    



### SQL LITE Requests


root = ""
definition = ""


def select(word):
    global root
    global definition
    global conn
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
        
        root = row[1]; 
        for r in row[2].split("|"):
            definition += r+"\n";
 


def dicOffLine(word):
    select(word)
    dicOFFLine = {
        'root'       : root ,            
        'definition' : definition 
    };
    return dicOFFLine;




    