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
    b[0] = b[0].replace('"', '')
    b[-1] = b[-1].replace('"','')

    if len(a) != len(b):
        return 0
    else:
        for x in b:
            if x in a:
                continue
            else:
                return 0
        return 1

a=[['работа','яндекс','такси','nice'],['яндекс','работа','такси']]
b=[['"работа','яндекс','такси"'],['работа','яндекс','такси']]

b_saved=[]
for x in b:
    b_saved.append(" ".join(x))

def analyze(srch, smnt):
    list_tmp = []
    for k in range(len(srch)):
        for i in range(len(smnt)):
            tmp = proverka(srch[k], smnt[i])
            if tmp == 0:
                continue
            else:
                list_tmp.append(b_saved[i])
                print('complete ', k, ' from all')
                break
        else:
            list_tmp.append('Unknown')
            print('complete ', k, ' from all')
    return list_tmp

print(analyze(a,b))