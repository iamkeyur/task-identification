import json
import math
from preprocess import Processor


def generate_vector(path, target):

    p = Processor('', 0)

    inverted_index = {}

    with open(path, 'r', encoding='utf-8') as source:
        raw = source.read()

    vector = json.loads(raw)
    doc_id = 0
    # print('doc count', len(vector))
    for doc in vector:
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


class Lexical:
    def __init__(self):
        pass

    def trigram(self, s):
        tri = set()

        if len(s) <= 3:
            tri.add(s)
        else:
            for i in range(len(s) - 2):
                tri.add(s[i:i+3])

        return tri

    def jaccard(self, s1, s2):
        c1 = self.trigram(s1)
        c2 = self.trigram(s2)

        return 1 - len(c1.intersection(c2)) / len(c1.union(c2))

    def levenshtein(self, seq1, seq2):
        one_ago = None
        this_row = list(range(1, len(seq2) + 1)) + [0]
        for x in range(len(seq1)):
            two_ago, one_ago, this_row = one_ago, this_row, [0] * len(seq2) + [x + 1]
            for y in range(len(seq2)):
                del_cost = one_ago[y] + 1
                add_cost = this_row[y - 1] + 1
                sub_cost = one_ago[y - 1] + (seq1[x] != seq2[y])
                this_row[y] = min(del_cost, add_cost, sub_cost)
                if x > 0 and y > 0 and seq1[x] == seq2[y - 1] and seq1[x - 1] == seq2[y] and seq1[x] != seq2[y]:
                    this_row[y] = min(this_row[y], two_ago[y - 2] + 1)

        # normalization using the average length of 2 strings
        return this_row[len(seq2) - 1] / max(len(seq1), len(seq2))

    def content_distance(self, s1, s2):
        return (self.jaccard(s1, s2) + self.levenshtein(s1, s2)) / 2


class Semantic:
    def __init__(self, path):
        self.count = 6043
        with open(path, 'r', encoding='utf-8') as source:
            self.vector = json.loads(source.read())

    def semantic_distance_wiki(self, s1, s2):
        v1 = self.get_total_vector(s1)
        v2 = self.get_total_vector(s2)

        return 1 - self.cosine(v1, v2)

    def get_total_vector(self, s):
        l = s.split()
        vector = {}
        for term in l:
            v = self.get_vector(term)
            for d in v:
                if d in vector:
                    vector[d] += v[d]
                else:
                    vector[d] = v[d]

        return vector

    def get_vector(self, term):
        return self.vector.get(term, {})

    def cosine(self, v1, v2):
        dot_product = 0
        norm_1, norm_2 = self.norm(v1), self.norm(v2)
        for d in v1:
            if d in v2:
                dot_product += v1[d] * v2[d]

        if norm_1 == 0 or norm_2 == 0:
            return 0
        else:
            return dot_product / (norm_1 * norm_2)

    def norm(self, v):
        n = 0
        for d in v:
            n += v[d] ** 2

        return math.sqrt(n)

if __name__ == '__main__':
    s1 = 'honda accord fuel addit check engin light'
    s2 = 'honda accord check engin light pa emiss'

    # generate_vector('/Users/susen/Projects/cs290n/intermediate/all.txt',
    #                 '/Users/susen/Projects/cs290n/intermediate/index.txt')

    s = Semantic('/Users/susen/Projects/cs290n/intermediate/index.txt')
    l = Lexical()
    print(s.semantic_distance_wiki(s1, s2))
    print(l.content_distance(s1, s2))
