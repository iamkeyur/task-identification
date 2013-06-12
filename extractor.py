from multiprocessing import Pool
from time import time
from nltk.util import clean_html
import nltk
import os
from bs4 import BeautifulSoup
import json
from preprocess import Processor

def occurrence(word):
    return [(word, 1)]


def occurrenceCount(keyVal):
    return keyVal[0], sum(keyVal[1])


# try to use a parallel method
class MapReduce(object):

    def __init__(self, mapper, reducer, numProcs=None):
        self.mapper = mapper
        self.reducer = reducer
        self.pool = Pool(numProcs)

    @staticmethod
    def partition(intermediate1):
        dct = {}

        for lst in intermediate1:
            for key, value in lst:
                if key in dct:
                    dct[key].append(value)
                else:
                    dct[key] = [value]

        return dct.items()

    def process(self, data):
        intermediate1 = self.pool.map(self.mapper, data)
        intermediate2 = MapReduce.partition(intermediate1)
        return self.pool.map(self.reducer, intermediate2)


def word_count(s):
    soup = BeautifulSoup(s)
    imm = soup.find_all(id='bodyContent')
    if len(imm) > 0:
        raw = soup.find_all(id='bodyContent')[0].get_text()
    else:
        raw = ''

    wl = nltk.word_tokenize(raw)

    vector = dict()
    for token in wl:
        if token in vector:
            vector[token] += 1
        else:
            vector[token] = 1

    return vector


def reader(path, target):
    id = 0
    list_dirs = os.walk(path)
    data = []

    for root, dirs, files in list_dirs:
        for f in files:
            if f[-4:] != 'html':
                continue

            with open(os.path.join(root, f), 'r', encoding='utf-8') as html:
                v = word_count(html.read())
                print(id)
                data.append(v)

            id += 1

    with open('{}/{}.txt'.format(target, 'all'), 'w') as vector:
        vector.write(json.dumps(data))


def buf_reader(path, target):
    id = 0
    list_dirs = os.walk(path)
    # data = []

    vector = open('{}/{}.txt'.format(target, 'all_large'), 'w')

    for root, dirs, files in list_dirs:
        for f in files:
            if f[-4:] != 'html':
                continue

            with open(os.path.join(root, f), 'r', encoding='utf-8') as html:
                v = word_count(html.read())
                print(id)
                #data.append(v)
                vector.write(json.dumps(v) + '\n')

            id += 1


def buf_generate_vector(path, target):

    p = Processor('', 0)

    inverted_index = {}
    vector = []

    with open(path, 'r', encoding='utf-8') as source:
        doc_id = 0
        # print('doc count', len(vector))
        for line in source:
            print(doc_id)
            doc = json.loads(line[:-1])
            for term in doc:
                tidy = p.trim(term).lower()
                if tidy != '':
                    t = p.remove_stop_words(tidy)
                    t = p.porter_stemming(t)
                    if t != '':
                        if t in inverted_index:
                            inverted_index[t][doc_id] = doc[term]
                        else:
                            inverted_index[t] = {doc_id: doc[term]}

            doc_id += 1

    with open(target, 'w', encoding='utf-8') as dst:
        dst.write(json.dumps(inverted_index))

if __name__ == '__main__':

    #reader('/Users/susen/Projects/cs290n/en/', '/Users/susen/Projects/cs290n/intermediate/')
    #buf_reader('/Users/susen/Projects/cs290n/en/', '/Users/susen/Projects/cs290n/intermediate/')
    buf_generate_vector('/Users/susen/Projects/cs290n/intermediate/all_large.txt',
                        '/Users/susen/Projects/cs290n/intermediate/index_large.txt')