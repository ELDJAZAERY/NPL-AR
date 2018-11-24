# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 17:22:32 2018

@author: ELDJAZAERY

"""


import requests
from bs4 import BeautifulSoup


### --------- OnLine Part ----------- ### 

url = 'https://www.almaany.com/ar/dict/ar-ar/';
path = 'XMLDIC/';

def definition(word):
    r = requests.get(url+word)

    # index of begin and end (def) 
    indexDMR = r.text.find('''<ol class="meaning-results">''');
    indexFMR = r.text[indexDMR:].find('</ol>') + indexDMR;
    
    # if exist
    if(indexDMR < indexFMR):
        result = r.text[indexDMR:indexFMR];
    else:
        return '';
        
    
    soup = BeautifulSoup(result,'lxml');
    
    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("   "))
    
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    lines = text.splitlines();
    definition = '\n'.join(line for line in lines if(len(line)<150));
    
    return definition;


def relativeWords(word):
    r = requests.get(url+word)
    # index of begin and end (Relative words) 
    indexDRW = r.text.find('''كلمات ذات صلة''');
    indexFRW = r.text[indexDRW:].find('</ul>') + indexDRW;
    
    # if exist
    if(indexDRW < indexFRW):
        result = r.text[indexDRW:indexFRW];
    else:
        return '';
    
    soup = BeautifulSoup(result,'lxml');
    
    # get text
    text = soup.get_text()
    
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    
    # drop blank lines
    RW = '\n'.join(chunk for chunk in chunks if chunk)
    
    return RW;

def nearWords(word):
    r = requests.get(url+word)
    # index of begin and end (Relative words) 
    indexDRW = r.text.find('''كلمات قريبة''');
    indexFRW = r.text[indexDRW:].find('</ul>') + indexDRW;
    
    # if exist
    if(indexDRW < indexFRW):
        result = r.text[indexDRW:indexFRW];
    else:
        return '';
    
    soup = BeautifulSoup(result,'lxml');
    
    # get text
    text = soup.get_text()
    
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("   "))
    
    # drop blank lines
    NW = '\n'.join(chunk for chunk in chunks if chunk)
    
    return NW;


def dicOnLine(word):
    definitiononline = definition(word)
    relativeWordsonLine = relativeWords(word)
    nearWordsOnLine = nearWords(word)
    dicOnLine = {
        'definition'    : definitiononline ,
        'relativeWords' : relativeWordsonLine,
        'nearWords'     : nearWordsOnLine
    };
    return dicOnLine;


import socket
def internet():
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False



### ------------ OfLine Part ---------- ### 


def dicOffLine(word):
    definitiOFFonline      = '' ##definitionOFFLine(word)
    relativeWordsOFFLine   = '' ##relativeWordsOFFLine(word)
    nearWordsOFFLine       = '' ##nearWordsOFFLine(word)
    dicOFFLine = {
        'definition'    : definitiOFFonline ,
        'relativeWords' : relativeWordsOFFLine,
        'nearWords'     : nearWordsOFFLine
    };
    return dicOFFLine;

import xml.etree.ElementTree
def definitionOFFLine(word):
    e = xml.etree.ElementTree.parse('ArDict.xml').getroot()
    print(e);

def relativeWordsOFFLine(word):
    print("");

def nearWordsOFFLine(word):
    print("");


### ------------ main Part ---------- ### 

def DicOnOFF(word):
    try:
        internet()
        return dicOnLine(word);
    except:
        return dicOffLine(word);


word = 'اكل';
definitionOFFLine(word);