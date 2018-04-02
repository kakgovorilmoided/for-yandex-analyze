from v2 import functions as func, KeyClasses
import csv


keys = func.read_from_csv('../semantic_new.csv', 'keyword_name:')
# keys = func.read_from_csv('../searches.csv', 'Ключевик')
phrases = func.read_from_csv('../searches.csv', 'Поисковая фраза (Директ)')
phrases3d = func.phrases_to_normed_matrix(phrases)
keys_classes = func.keys_to_normed_matrix(keys)


csv_data = list(csv.reader(open('../searches.csv', encoding='utf-8')))

for p in range(len(phrases3d)):
    for key in keys_classes:
        result = key.analyse(phrases3d[p])
        if result:
            csv_data[p+1][2] = key.base_key

writer = csv.writer(open("../output.csv", 'w',  encoding='utf-8'))
writer.writerows(csv_data)
