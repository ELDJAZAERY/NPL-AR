# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from   lxml import etree
import tashaphyne.arabic_const as arabconst
import pickle
import codecs
import re



### GLOBALS VARS ###

corpus_path = 'data/Corpus/';
inverses_Base_path = 'data/Inverses';


#corpus_path = 'Corpus/';
#inverses_Base_path = 'Inverses';


types = { 'chiir':'شعر' , 'Nathr':'نثر'}
types = { 'chiir':'شعر'}


sents_patern = r'(?<=[.;?!؟])\s'



normalized_Search = False;


### Normalization

def Normalisation(text):
   text = arabconst.HARAKAT_PAT.sub('', text)
   text = re.sub(r'[%s]' % arabconst.TATWEEL,'', text)
   text = arabconst.ALEFAT_PAT.sub(arabconst.ALEF, text)
   text = arabconst.LAMALEFAT_PAT.sub(u'%s%s' % (arabconst.LAM, arabconst.ALEF), text)
   return text;




### overwrite the __contain__ function for normalize the text


def __contains__(word , txt):
    global normalized_Search
    if(normalized_Search):        
        txt = Normalisation(txt)
        
    return txt.__contains__(word)


def __find__(word , txt):
    global normalized_Search
    if(normalized_Search):        
        txt = Normalisation(txt)
    return txt.find(word)    
    
### recherche functions ####

## Boolean search
def boolean(list_text,word):
    global sents_patern
    print("Bolean")
    for txt in list_text:
        #sentences = txt.split('\n')
        sentences = re.split(sents_patern,txt);
        for sent in sentences:
            if(__contains__(word,sent)): return sent;

    return ''


## cheked the order of request in the text  
def vectorielOrdreChecker(text,request):
    global sents_patern
    sentences = re.split(sents_patern, text);
    #sentences = text.split('\n')
    ReqToken = request.split();
    print("vectorielOrdreChecker")
    for sent in sentences:
        index = -2;
        matched = True;
        originSent = sent;
        for token in ReqToken:
            index = __find__(token,sent);
            sent = sent[index:]
            if(index == -1): matched = False; break; 
        if(matched): return originSent;
        
    return '';

## checke the presence only in one sent
def vectorielSents(text,request):
    global sents_patern
    sentences = re.split(sents_patern, text);
    #sentences = text.split('\n')
    ReqToken = request.split();
    
    print("vectorielSents")
    
    for sent in sentences:
        nbToken = 0;
        for t in ReqToken:
            if(__contains__(t,sent)): nbToken += 1;
            else : break;
        if(nbToken == len(ReqToken)): return sent;

    return '';


def vectorielMS(text,request):
    global sents_patern
    sentences = re.split(sents_patern, text);
    #sentences = text.split('\n')
    ReqToken = request.split();
    
    print("vectorielMS")
    examples = set();
    #contin = True;
    for t in ReqToken:
        #if(not contin): contin = True ; continue;
        for sent in sentences:
            if(__contains__(t,sent)):
                examples.add(sent)
                #contin = False;
                break;

    return '\n'.join(examples);
    



## checke the presence without any condition
def vectoriel(text,request):
    ReqToken = request.split();
    print("vectoriel")
    indexs = set();
    for token in ReqToken:
        idx = __find__(token,text);
        if(idx == -1): return ''
        indexs.add(idx)
        
    indexs = list(sorted(indexs));
    sent = text[indexs[0]:indexs[len(indexs)-1]]
    return sent;
    



##### recherche functions #####


def getText(file):
    
    text = '';
    
    try:
        tree = etree.parse(file);
    except: print('\n\n### File Not Found ### \n --- '+file+' --- \n\n'); return ''
        
    root = tree.getroot()

    for child in root:
        if(child.text and child.tag == 'Content'):
            text += child.text;

    if(file.find('chiir') != -1):
        text = get_Chi3r_form(text);
    
    print(text)
    return text;

'''     
    soup = BeautifulSoup(text,'lxml');

    # get text
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("   "))
    
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    
    if(file.find('chiir') != -1):
        text = get_Chi3r_form(text);
    return text;
'''    
    


def get_Chi3r_form(text):
    chi3r = '';
    
    lines = text.split('\n');
    
    i = 0;
    bayt_chi3r = '';
    for line in lines:
        if(i == 2):
            chi3r += bayt_chi3r + ' . \n';
            bayt_chi3r = '';
            i = 0;
        else :
            bayt_chi3r += ' '+line;
            i += 1;
    
    return chi3r;

   

def intersect(*d):
    sets = iter(map(set, d))
    result = sets.next()
    for s in sets:
        result = result.intersection(s)
    return result

   
def files_Pertinants(expr,typ,Aaser,invers):
    expr = Normalisation(expr)
    listword = set(expr.split(" "))
    
    files  = []
    files2 = []
    words  = []
    words_manquqnts = []
    
    global corpus_path;
    
    if(Aaser == ''): files_dir = corpus_path + typ+'/' 
    else: files_dir = corpus_path + typ+'/' + Aaser + '/'
    
    # recup les mot et le fichier du dict qui exist dans l'expression
    with codecs.open(invers, 'rb') as read_file:
        dict = pickle.load(read_file)
        for w in listword:
#            for e in dict:
#                if(e[0].find(w) != -1):
#                    print(e[0] , w)
            fw = [files_dir+element[1]+'.xml' for element in dict if element[0]==w]
            if(len(fw) == 0): continue;
            files.append(fw)
            files2.append(list(set(files[0]).intersection(*files)))
            if(len(files2) == 0):
                #return (words,files);
                break;
            else:
                files = files2;
                #files2 = []
            
            words.append(w);
            
    if(len(files)): files = list(set(files[0]).intersection(*files))
    print('files finales' , len(files))
    print(files)
    for word in listword:
        if(not words.__contains__(word)):
            words_manquqnts.append(word)
    
    return (words_manquqnts,files);



def Extract_Example(files,Request):
    EXEMPLE = '';
        
    list_Texts = [];
    try:        
        for file in files:
            list_Texts.append(getText(file));
    except: pass
    
    if(len(Request.split(' ')) == 1):
        return boolean(list_Texts,Request);

    
    for text in list_Texts:
        EXEMPLE = vectorielOrdreChecker(text,Request);
        if(EXEMPLE != '' ): return EXEMPLE;
    

    for text in list_Texts:
        EXEMPLE = vectorielSents(text,Request);
        if(EXEMPLE != '' ): return EXEMPLE;
    

    for text in list_Texts:
        EXEMPLE = vectorielMS(text,Request);
        if(EXEMPLE != '' ): return EXEMPLE;
    

    for text in list_Texts:
        EXEMPLE = vectoriel(text,Request);
        if(EXEMPLE != '' ): return EXEMPLE;

    
    return EXEMPLE;


def get_invers_Osoor_For(Type):
    return [];


def recherche_Examples(Aaser,Request,mode):
    
    global normalized_Search
    normalized_Search = False;
    
    if(mode == 'Auto'):
        ## (Auto Mode)
        ## W'll Searched in Normalize Form if the user get a Normalized Request
        Request_Normalized = Normalisation(Request);
        if(Request_Normalized == Request):
            normalized_Search = True;
    else:
        ## (Normalize Mode)
        ## W'll Searched in Normalize Form
        if(mode == 'Normalize'):
            Request = Normalisation(Request);
            normalized_Search = True;
        
    ## ELSE
    ## (Brute Mode) --- default Mode ---
    ## W'll Searched in Brute Form
   
    
    if(Aaser == 'Quran' or Aaser == 'Hadith') : 
        return recherche_Examples_From_Quraan_Hadith(Aaser,Request)
    
    ## ESLE 
    
    EXAMPLES = {}    
    
    global types;
    global inverses_path;
    global corpus_path;
 
    fname = Aaser + 'inverse.txt'
    
    for typ in types:        
        invers_path = inverses_Base_path + '/'+ typ +'/' + Aaser+'/' + fname;
        files = files_Pertinants(Request,typ,Aaser,invers_path);
        if(len(files)):
            example = Extract_Example(files[1],Request)
            EXAMPLES[typ] = ( example , files[0] );
       
    
    '''
    EXAMPLES {
        chhir  : (example , word_manquants)
        nather : (example , word_manquants)
    }    
    '''
    
    return EXAMPLES



def recherche_Examples_From_Quraan_Hadith(frm,Request):
    EXAMPLES = {}
    
    global types;
    global inverses_path;
    global corpus_path;
 

    fname = frm+'inverse.txt'
    invers_path = inverses_Base_path + '/'+ frm +'/' + fname;    
            
    files = files_Pertinants(Request,frm,'',invers_path);
    if(len(files)):
        example = Extract_Example(files[1],Request)
        EXAMPLES[frm] = ( example , files[0] );
       
        
    '''
    type = Quraan OR Hadith
    EXAMPLES {
        type : (example , word_manquants)
    }    
    
    '''   
    
    return EXAMPLES


'''
aaser = 'العصر المملوكي'
#aaser = 'العصر الإسلامي'
#aaser = 'العصر الايوبي'
aaser = 'العصر الإسلامي'


## EXEMPLE 1
requet = 'كسر'
requet += ' '
requet += 'ناصب'
requet += ' '
requet += 'يبني'


## EXEMPLE 2

requet = 'مسراه'
requet += ' '
requet += 'كاسره'
requet += ' '
requet += 'الطيورل'

#requet = 'تَفتَّحُ'

requet = 'الورى'

#requet = 'لخالِدِ'

#requet = 'الورث'


print(recherche_Examples(aaser,requet,'Auto')['chiir'][0])
'''