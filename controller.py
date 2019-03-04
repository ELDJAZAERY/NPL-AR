# -*- coding: utf-8 -*-

from definition import defWord , sqlLite
from data import recherche
import re


def get_definition(word, OnLine):
    return defWord.Dict(word,OnLine)['definitions'];

def get_relatives_words(word, OnLine):
	return defWord.Dict(word, OnLine)['relativeWords'];
	

## get Examples dans un "Aasser precise"
types = { 'chiir':'شعر' , 'Nathr':'نثر' , 'Quran' : 'القرآن الكريم' , 'Hadith' : 'حديث شريف'}

def get_examples(word, aaser):
    global types
    EXEMPLES = []
    dict_example = recherche.recherche_Examples(aaser,word,'Auto');
    for typ in dict_example:
        exmpl , words_manquqnts = dict_example[typ]
        if(not len(exmpl)): continue;
        exmpl = types[typ] + ' :\n' + exmpl
        if(len(words_manquqnts)):
            exmpl += 'كلمات منقوصة : \n' + words_manquqnts.__str__()
        EXEMPLES.append(exmpl)
    return EXEMPLES;



def get_file_content(path):
    content = open(path, encoding="utf8").read()
    meta    = {}
    meta['era']      = re.search(r'<periode>(.*?)</periode>',     content).group(1)
    meta['category'] = re.search(r'<categorie>(.*?)</categorie>', content).group(1)
    meta['author']   = re.search(r'<auteur>(.*?)</auteur>',       content).group(1)
    meta['source']   = re.search(r'<source>(.*?)</source>',       content).group(1)
    
    content = re.sub('<\?xml.*?\?>', '', content)
    content = re.sub('<Meta(.|\n)*?</Meta>', '', content)
    content = re.sub('<Titrenorm(.|\n)*?</Titrenorm>', '', content)
    content = re.sub('<Contentnorm(.|\n)*?</Contentnorm>', '', content)
    content = re.sub('(<root>|</root>|<titre>|</titre>|<Content>|</Content>)', '', content)
    
    
    return (meta, content)


# Adds entries of random words to the dictionary
def generate_entries(nb_words, hist_dict, eras_names, is_online):
    words = sqlLite.get_random_words(nb_words,hist_dict)
    for w in words:    
        #deff = get_definition(w,is_online)
        #if(deff): deff = deff[0]    
        eras = {}
        for era in eras_names:
            #eras[era] = (deff, get_examples(w, era))
            eras[era] = ('', get_examples(w, era))
        hist_dict[w] = (False, eras)    
    return words	

