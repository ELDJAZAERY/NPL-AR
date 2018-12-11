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


roots = set()
definition = []
relativeWords = set()
nearWords = []



def select(word):
    global conn
    global definition
    global relativeWords
    global roots
    
    
    definition = [];
    roots = set();
    relativeWords = set();
    #nearWords = set();
    
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
    
    temp = ''
    for row in rows:
        if(row[1]): roots.add(row[1]);
        for r in row[2].split("|"):
            if( (r.__contains__('(فعل)') or
                 r.__contains__('(اسم)') or
                 r.__contains__('(حرف)') or
                 r.__contains__('(ضمير)') or
                 r.__contains__('(حرف)') or
                 r.__contains__('(حرف/اداة)') or
                 r.__contains__('(فعل: ثلاثي لازم)') ) and temp != '' ):
                
                definition.append(temp)
                temp = '';
                
            temp += r+'\n';
            
        definition.append(temp)
        
    selectRelativeWords()

def selectRelativeWords():
    global conn
    global roots
    global relativeWords

    cur = conn.cursor()
    print(roots)
    for root in roots:
        request = '''
                select word from WordsTable where root = "'''+root+'''"
        '''
        cur.execute(request)
        rows = cur.fetchall()
    
        for row in rows:
            relativeWords.add(row[0])


def dicOffLine(word):
    select(word)
    dicOFFLine = {
        'connexion'     : False,
        'definitions'   : definition ,
        'relativeWords' : relativeWords,
        'nearWords'     : []
    };
    return dicOFFLine;


