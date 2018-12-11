# -*- coding: utf-8 -*-
"""
Created on Sat Nov  1 13:52:21 2018

@author: EL DJAZAERY Ibrahim
"""



word = 'دخداخ';
word = 'اكل'
word = 'أن'
#word = 'إن'
#word = 'اكخس'


import defWord


## 2eme paramettre sert a force l'utilisation de database local malgre il y a connexion
result = defWord.Dict(word,True);  ## local data base qlq soit ida kayen cnx ou nn
result = defWord.Dict(word,False); ## local data base or onLine data base 3la hssab ida kayen cnx ou nn


## resulta returne sous form de dict
'''
result = {
    'connexion'     : True or False,
    'definitions'   : List of Deffinitions ,
    'relativeWords' : List of Relative words ## les mote li 3ndhom mm champ lexical avec le mot rechercher
    'nearWords'     : List of near words ## ida le mots ma y'existich yproposilo des mots qrb syntaxique (OnLine only) off line tkon vide
};
'''



## extracts les definitions (on / OFF line)

print('connexion -> ',result['connexion'])







### Model Vectoriel 


'''

voir modelV.py

## le model vectoriel rah yreturnilna qlq docs
## pour chaque doc mn hado appelle la function vectorielOrdreChecker w ida returnate null f ga3 les docs 
## pour chaque doc appelle la function vectorielSents et if tjrs return null pour tt les docs
## utiliser la function vectoriel


la function vectorielOrdreChecker lazem ykono kamel f mm phrase w par ordre
la function vectorielSents lazem ykono kamel f mm phrase
la function vectoriel ykono kaynin w khlass

w ida thebo tzido les cas qololi brk

w kayen 2 example dessous 


PPPPPPPPSSSSSS :
    appelles les function bla text normalizer w el resultat li ttreturna mena edi l'equivqlqnce tq3hq ml txt brute

'''








### Main ###


## extract the normalize text from each file of vectorial model and cheked thers one by one
## the first one who return a sentence et non pas None return this sentence
        
## example le model vectoriel returnaly 4 files
## for each file
##   result = vectorielOrdreChecked( file.normalizeText , Request )
##  if( result != non  ) return result (Affichi hadi la sentence )



text = '''
يعرّف العصر الجاهلي بالفترة 
الممتدّة قبل بعثة سيّدنا محمّد صلّى الله عليه وسلّم، والّتي استمرّت قرن ونصف أو مئتان قبل البعثة . سمّي بالعصر 
الجاهلي لما شاع فيه من الجهل، بسبب جهل الناس بعقيدة إبراهيم عليه السّلام، فسُمّوا جاهليّين، وليس المقصود 
بالجهل الّذي هو ضد العلم بل الجهل الّذي ضدّ الحلم . عبد العرب في العصر الجاهلي الأوثان و الأصنام، ومن أشهر 
أصنامهم في العصر الجاهلي: هبل- الّلات- العزّى- مناة، كما أنّ كثيراً من العرب من عبدوا الشّمس والقمر 
والنّجوم، وكان هناك فئة لم تعجبهم سخافات الوثنيّة وهدتهم فطرتهم، فعدلوا عن عبادة 
الأصنام وعبدوا الله على ملّة إبراهيم عليه السّلام، وكانوا يسمون (الحنفاء) .
'''


requestte =  "جهل وليس العلم"

import modelV


## exemple 1

print('vectorielOrdreChecked')
print(modelV.vectorielOrdreChecker(text,requestte))
print('\n')


print('vectorielSents')
print(modelV.vectorielSents(text,requestte))
print('\n')


print('vectoriel')
print(modelV.vectoriel(text,requestte))
print('\n')




# exemple 2

requestte = "العلم وليس جهل ";


print('vectorielOrdreChecked')
print(modelV.vectorielOrdreChecker(text,requestte))
print('\n')


print('vectorielSents')
print(modelV.vectorielSents(text,requestte))
print('\n')


print('vectoriel')
print(modelV.vectoriel(text,requestte))
print('\n')

