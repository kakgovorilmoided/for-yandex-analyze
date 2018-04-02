import pandas as pd
import pymorphy2
from v2 import KeyClasses


def read_from_csv(file_path, column_name):
    data = pd.read_csv(file_path, encoding='utf-8')
    column = data[column_name].values
    list_keys = list()
    for cell in column:
        list_keys.append(cell.lower())
    return list_keys


def init_list_as_dict(l):
    d = dict()
    for item in l:
        d[item] = False
    return d


def phrases_to_normed_matrix(input_list):
    words_matrix = list(list(list()))
    morph = pymorphy2.MorphAnalyzer()
    for item in input_list:
        words = item.split()
        words_normed = list()
        for word in words:
            normed = morph.parse(word)[0].normal_form
            not_normed = word
            words_save_list = list()
            words_save_list.append(not_normed)  # not normed word first index
            words_save_list.append(normed)  # normed word second index
            words_normed.append(words_save_list)
        words_matrix.append(words_normed)
    return words_matrix


def keys_to_normed_matrix(input_list):
    words_matrix = list()
    for item in input_list:
        if '"' in item:
            key_class = KeyClasses.KeyQuotes()
        if '[' in item and ']' in item:
            key_class = KeyClasses.KeyBrackets()
        if '[' not in item and ']' not in item and '"' not in item:
            key_class = KeyClasses.KeySimple()
        key_class.init_key(item)
        words_matrix.append(key_class)

    return words_matrix

