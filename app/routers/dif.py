import pandas as pd
from nltk.tokenize import word_tokenize
import pymorphy2
from multiprocessing import Process, Pool
import os

df = pd.read_csv('eda.csv')


def verbs(text):
    tokens = word_tokenize(text, language="russian")
    actions = 0
    for i in tokens:
        morph = pymorphy2.MorphAnalyzer()
        p = morph.parse(i)[0]
        if p.tag.POS == 'VERB' or p.tag.POS == 'INFN' or p.tag.POS == 'GRND':
            actions += 1
    return actions


def dif_calc(row):
    ingr = sum(map(str.isupper, row[1]["list_ingrid"]))
    list_rec = [num for num in row[1]['list_resipe'].split('.') if len(num) <= 2 and num.isdigit()]
    steps = int(list_rec[-1])
    difficulty = round(int(verbs(row[1]['list_resipe']))*ingr/steps, 2)
    return difficulty


def dif_write(row):
    new_df = pd.DataFrame({'id': [row[1]["id"]],
                           'name': [row[1]["name"]],
                           'difficulty': dif_calc(row)})
    new_df.to_csv('dif.csv', mode='a', index=False, header=False)


if __name__ == '__main__':
    with Pool() as pool:
        pool.map(dif_write, df.iterrows())
