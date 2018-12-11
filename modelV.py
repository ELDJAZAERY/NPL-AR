# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 15:37:06 2018

@author: EL DJAZAERY
"""

from nltk.tokenize import WhitespaceTokenizer
import re

tokenizer= WhitespaceTokenizer()


## cheked the order of request in the text  
def vectorielOrdreChecker(text,request):
    sentences = re.split(r'(?<=[.;?!؟])\s', text);
    ReqToken = request.split();
    for sent in sentences:
        index = -2;
        matched = True;
        originSent = sent;
        for token in ReqToken:
            index = sent.find(token);            
            sent = sent[index:]
            if(index == -1): matched = False; break; 
        if(matched): return originSent;


## checke the presence only in one sent
def vectorielSents(text,request):
    sentences = re.split(r'(?<=[.;?!؟])\s', text);
    ReqToken = request.split();
    for sent in sentences:
        nbToken = 0;
        for t in ReqToken:
            if(sent.__contains__(t)): nbToken += 1;
            else : break;
        if(nbToken == len(ReqToken)): return sent;




## checke the presence without any condition
def vectoriel(text,request):
    ReqToken = request.split();
    
    indexs = set();
    for token in ReqToken:
        idx = text.find(token);
        if(idx == -1): return ''
        indexs.add(idx)
        
    indexs = list(sorted(indexs));
    sent = text[indexs[0]:indexs[len(indexs)-1]]
    return sent;



