import pymorphy2
import numpy as np
from v2 import functions as func


# double quotes key process class
class KeyQuotes:
    def __init__(self):
        self.base_key = ''
        self.plus_words = list()
        self.solid_words = list()
        self.words = list()
        self.count = -1

    def init_key(self, key):
        morph = pymorphy2.MorphAnalyzer()
        self.base_key = key

        ind_begin = int(key.index('"') + 1)
        ind_end = int(key.rfind('"'))
        words_in_quotes = key[ind_begin:ind_end]
        words = words_in_quotes.split()
        self.count = len(words)

        for word in words:
            if '+' in word:
                self.plus_words.append(word.replace('+', ''))
                continue
            if '!' in word:
                self.solid_words.append(word.replace('!', ''))
                continue
            self.words.append(morph.parse(word)[0].normal_form)

    def analyse(self, phrase):

        list_first_word = list()
        for item in phrase:
            list_first_word.append(item[0])
        unique = np.unique(list_first_word)

        plus_dict = func.init_list_as_dict(self.plus_words)
        solid_dict = func.init_list_as_dict(self.solid_words)
        words_dict = func.init_list_as_dict(self.words)

        if int(len(unique)) != int(self.count):
            return False
        for word in phrase:
            if word[0] in plus_dict:
                plus_dict[word[0]] = True
                continue
            if word[0] in solid_dict:
                solid_dict[word[0]] = True
                continue
            if word[1] in words_dict:
                words_dict[word[1]] = True
                continue

        if False in plus_dict.values():
            return False
        if False in solid_dict.values():
            return False
        if False in words_dict.values():
            return False
        return True


# types: +, !,
class OrderedWords:
    def __init__(self, word, normed_word, word_type):
        self.word = word
        self.normed_word = normed_word
        self.type = word_type

    def __hash__(self):
        return hash((self.word, self.normed_word, self.type))

    def __eq__(self, other):
        return (self.word, self.normed_word, self.type)\
               == (other.word, other.normed_word, other.type)

    def __ne__(self, other):
        return not (self == other)


# double square brackets process class
class KeyBrackets:
    def __init__(self):
        self.base_key = ''
        self.plus_words = list()
        self.solid_words = list()
        self.minus_words = list()
        self.ordered_words = list()
        self.words = list()

    def init_key(self, key):
        morph = pymorphy2.MorphAnalyzer()
        self.base_key = key

        # process word in brackets - ordered words
        ind_begin = int(key.index('[') + 1)
        ind_end = int(key.rfind(']'))
        words_in_brackets = key[ind_begin:ind_end]
        words = words_in_brackets.split()
        for word in words:
            if '!' in word:
                save_word = OrderedWords(word, '', '!')
                self.ordered_words.append(save_word)
                continue
            if '+' in word:
                save_word = OrderedWords(word, '', '+')
                self.ordered_words.append(save_word)
                continue
            save_word = OrderedWords(word, morph.parse(word)[0].normal_form, '')
            self.ordered_words.append(save_word)

        modified_key = key.replace('[' + words_in_brackets + ']', '')
        rest_words = modified_key.split()
        for word in rest_words:
            if '+' in word:
                self.plus_words.append(word.replace('+', ''))
                continue
            if '!' in word:
                self.solid_words.append(word.replace('!', ''))
                continue
            if word.startswith('-'):
                self.minus_words.append(word.replace('-', ''))
                continue
            self.words.append(morph.parse(word)[0].normal_form)

    def analyse(self, phrase):
        plus_dict = func.init_list_as_dict(self.plus_words)
        solid_dict = func.init_list_as_dict(self.solid_words)
        minus_dict = func.init_list_as_dict(self.minus_words)
        words_dict = func.init_list_as_dict(self.words)

        ordered_dict = dict()
        for ordered_elem in self.ordered_words:
            ordered_dict[ordered_elem] = False

        was_ordered_check = False
        for i in range(len(phrase)):
            if not was_ordered_check and self.check_in_ordered(phrase[i], ordered_dict):
                was_ordered_check = True
                i = i + 1
                while i < len(phrase) and self.check_in_ordered(phrase[i], ordered_dict):
                    i = i + 1
            if i >= len(phrase):
                break

            if phrase[i][0] in plus_dict:
                plus_dict[phrase[i][0]] = True
                continue
            if phrase[i][0] in solid_dict:
                solid_dict[phrase[i][0]] = True
                continue
            if phrase[i][1] in words_dict:
                words_dict[phrase[i][1]] = True
                continue
            if phrase[i][0] in minus_dict:
                minus_dict[phrase[i][1]] = True
                continue

        if False in plus_dict.values():
            return False
        if False in solid_dict.values():
            return False
        if False in words_dict.values():
            return False
        if True in minus_dict.values():
            return False
        if False in ordered_dict.values():
            return False
        return True

    def check_in_ordered(self, word, ordered_dict):
        for ordered_elem in self.ordered_words:
            if ordered_elem.type == '!' or ordered_elem.type == '+':
                if ordered_elem.normed_word == word[1]:
                    ordered_dict[ordered_elem] = True
                    return True
            else:
                if ordered_elem.word == word[0]:
                    ordered_dict[ordered_elem] = True
                    return True
        return False


# simple words process class
class KeySimple:
    def __init__(self):
        self.base_key = ''
        self.plus_words = list()
        self.solid_words = list()
        self.minus_words = list()
        self.words = list()

    def init_key(self, key):
        self.base_key = key

        morph = pymorphy2.MorphAnalyzer()
        words = key.split()
        for word in words:
            if '+' in word:
                self.plus_words.append(word.replace('+', ''))
                continue
            if '!' in word:
                self.solid_words.append(word.replace('!', ''))
                continue
            if word.startswith('-'):
                self.minus_words.append(word.replace('-', ''))
                continue
            self.words.append(morph.parse(word)[0].normal_form)

    def analyse(self, phrase):
        plus_dict = func.init_list_as_dict(self.plus_words)
        solid_dict = func.init_list_as_dict(self.solid_words)
        minus_dict = func.init_list_as_dict(self.minus_words)
        words_dict = func.init_list_as_dict(self.words)

        for word in phrase:
            if word[0] in plus_dict:
                plus_dict[word[0]] = True
                continue
            if word[0] in solid_dict:
                solid_dict[word[0]] = True
                continue
            if word[1] in words_dict:
                words_dict[word[1]] = True
                continue
            if word[0] in minus_dict:
                words_dict[word[0]] = True
                continue

        if False in plus_dict.values():
            return False
        if False in solid_dict.values():
            return False
        if False in words_dict.values():
            return False
        if True in minus_dict.values():
            return False
        return True
