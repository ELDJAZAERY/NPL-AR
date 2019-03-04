# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 17:22:32 2018

@author: ELDJAZAERY

"""


import requests
from bs4 import BeautifulSoup


### --------- OnLine Part ----------- ### 

url = 'https://www.almaany.com/ar/dict/ar-ar/';


### ----- Check Connection internet ------- ###
import socket
def internet():
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False


### Normalization
import tashaphyne.arabic_const as arabconst
import re
def Normalisation(text):
   text = arabconst.HARAKAT_PAT.sub('', text)
   text = re.sub(r'[%s]' % arabconst.TATWEEL,'', text)
   text = arabconst.ALEFAT_PAT.sub(arabconst.ALEF, text)
   text = arabconst.LAMALEFAT_PAT.sub(u'%s%s' % (arabconst.LAM, arabconst.ALEF), text)
   return text;

### --------- < On Line Traitement >
def definition(word):
    print('avant ----------')
    r = requests.get(url+word)
    print('apreeeees ----------')

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
    
    definitions = set()
    temp = ''
    
    for line in lines:
        #if(len(line) > 200 ): continue;
        if( (line.__contains__('(فعل)') or line.__contains__('(اسم)') or line.__contains__('(حرف/اداة)')) and temp != '' ):
            definitions.add(temp)
            temp = '';
        temp += line+'\n';
        
    definitions.add(temp)
    
    return definitions;



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
    
    RWs = set([chunk for chunk in chunks if chunk and chunk != 'كلمات ذات صلة' and chunk != ' '])
    
    return RWs;



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
    
    NWs = set([chunk for chunk in chunks if chunk and chunk != 'كلمات قريبة' and chunk != ' '])
    
    return NWs;


def dicOnLine(word):
    definitiononline = definition(word)
    #RWs = relativeWords(word)
    #NWs = nearWords(word)
    dicOnLine = {
        'connexion'     : True,
        'definitions'   : definitiononline ,
#        'relativeWords' : RWs,
#        'nearWords'     : NWs
    };
    return dicOnLine;


### --------- </On Line Traitement>



### --------- <OFF Line Traitement>
from definition import sqlLite
def dicOffLine(word):
    return sqlLite.dicOffLine(word);

### --------- </OFF Line Traitement>




### ------------ main Function ---------- ### 


def Dict(word , OnLine):
    
    word = Normalisation(word)

    if(not OnLine): return dicOffLine(word);
    
    internet_enable = internet();
    if(internet_enable):
        return dicOnLine(word);
    else:
        return dicOffLine(word);
    
### ------------ main Function ---------- ### 

