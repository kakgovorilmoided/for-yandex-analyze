import pymorphy2


morph = pymorphy2.MorphAnalyzer()
print(morph.parse('заработать')[0].normal_form)