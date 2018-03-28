import pymorphy2
import pandas as pd

morph = pymorphy2.MorphAnalyzer()
def normed_word(x):
    p = morph.parse(x)[0]
    return p.normal_form

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
    b1=b
    b1[0] = b1[0].replace('"', '')
    b1[-1] = b1[-1].replace('"','')
    if (len(a)-len(b1)) == 0:
        print('dlina')
        for x in b1:
            if x in a:
                continue
            else:
                return 0
        return 1
    else:
        return 0

a=[['работа','яндекс','такси','nice'],['яндекс','работа','такси','Курган']]
b=[['"работа','яндекс','такси"'],['работа','яндекс','такси']]

b_saved=[]
for x in b:
    b_saved.append(" ".join(x))

def analyze(srch, smnt):
    list_tmp = []
    for x in srch:
        for i in range(len(smnt)):
            print(proverka(x,smnt[i]))
            if proverka(x, smnt[i]) == 0:
                print('ne vyshlo ', i)
                continue
            else:
                list_tmp.append(b_saved[i])
                break
        else:
            list_tmp.append('Unknown')
    print('done')
    return list_tmp

print(analyze(a,b))
