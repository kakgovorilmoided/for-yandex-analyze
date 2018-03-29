import pymorphy2
import pandas as pd

morph = pymorphy2.MorphAnalyzer()
def normed_word(x):
    p = morph.parse(x)[0]
    return p.normal_form


def proverka(a, b):
    if '"' in b[0]:
        return tochnaya_proverka(a, b)
    if '[' in b[0]:
        return kvadrat_proverka(a,b)
    else:
        for x in b:
            if x in a:
                continue
            else:
                return 0
        return 1


def kvadrat_proverka(a, b):
    b1 = []
    tmp = []
    for x in b:
        b1.append(x)
    b1[0] = b1[0].replace('[', '')
    b1[-2] = b1[-2].replace(']','')
    if b1[-1] in a:
        for i in range(len(b1) - 1):
            if b1[i] in a:
                tmp.append(b1[i])
            else:
                return 0
        b1.remove(b1[-1])
        for i in range(len(tmp)):
            if tmp[i] != b1[i]:
                return 0
        else:
            return 1
    else:
        return 0


def tochnaya_proverka(a, b):
    b1 = []
    for x in b:
        b1.append(x)
    b1[0] = b1[0].replace('"', '')
    b1[-1] = b1[-1].replace('"', '')
    if len(a) != len(b1):
        return 0
    else:
        for elem in b1:
            if elem in a:
                continue
            else:
                return 0
        return 1


a=[['работа','яндекс','такси','Воронеж'],['яндекс','работа','такси','Курган']]
b=[['[работа','яндекс','такси]', 'Воронеж'],['[работа','яндекс','такси]']]

print(proverka(a[0],b[0]))
