from multiprocessing import Pool
from time import time
from nltk.util import clean_html
import nltk


def occurrence(word):
    return [(word, 1)]


def occurrenceCount(keyVal):
    return keyVal[0], sum(keyVal[1])


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
    # t1 = time()
    raw = clean_html(s)
    # t2 = time()
    wl = nltk.word_tokenize(raw)
    # t3 = time()

    # print(t2 - t1, t3 - t2)

    vector = dict()
    for token in wl:
        if token in vector:
            vector[token] += 1
        else:
            vector[token] = 1

    return vector


if __name__ == '__main__':

    with open('/Users/susen/Projects/cs290n/en/articles/a/g/f/Agfa_Optima_1535_Sensor_2732.html', 'r') as html:
        v = word_count(html.read())
        print(v)