import numpy as np
import pandas as pd
import csv
import pymorphy2

#Functions

def proverka(a, b):
    if '"' in b[0]:
        return tochnaya_proverka(a, b)
    else:
        for x in b:
            if x in a:
                continue
            else:
                return 0
        return 1



def tochnaya_proverka(a, b):
    b1 = []
    for x in b:
        b1.append(x)
    b1[0] = b1[0].replace('"', '')
    b1[-1] = b1[-1].replace('"','')
    if len(a) != len(b1):
        return 0
    else:
        for elem in b1:
            if elem in a:
                continue
            else:
                return 0
        return 1


morph = pymorphy2.MorphAnalyzer()
def normed_word(x):
    p = morph.parse(x)[0]
    return p.normal_form


semantic = [] #our semantic kernal as list
searches = [] #our searches as list

#Считываем

df1 = pd.read_csv('semantic.csv', encoding='utf-8')
strings = df1['keyword_name:'].values
for row in strings:
    semantic.append(row)

df2 = pd.read_csv('searches.csv', encoding='utf-8')

strings = df2['searches'].values
for row in strings:
    searches.append(row)

semantic_saved=[]
for x in semantic:
    semantic_saved.append(x)

#Parsing

for i in range(len(semantic)):
    semantic[i] = semantic[i].split()
    for j in range(len(semantic[i])):
        semantic[i][j] = normed_word(semantic[i][j])
print('---------!semantic parsed!---------')

print(semantic)

for i in range(len(searches)):
    searches[i] = searches[i].split()
    for j in range(len(searches[i])):
        searches[i][j] = normed_word(searches[i][j])
print('---------!searches parsed!---------')
print(searches)


#Analyzing

def analyze(srch,smnt):

    list_tmp=[]
    for k in range(len(srch)):
        for i in range(len(smnt)):
            tmp = proverka(srch[k],smnt[i])
            if tmp == 0:
                continue
            else:
                list_tmp.append(semantic_saved[i])
                print('complete ', k,' from all')
                break
        else:
            list_tmp.append('Unknown')
            print('complete ', k, ' from all')
    return list_tmp


df2['predictions'] = analyze(searches, semantic)

df2.to_csv('result.csv')