import re

from PorterStemmer import PorterStemmer


class Processor:
    def __init__(self, path, num_records):
        self.porter = PorterStemmer()
        self.stop = set()
        with open('stop.words.dat', 'r') as sw:
            for line in sw:
                self.stop.add(line[:-1])

        self.process(path, num_records)

    def process(self, path, num_records):
        with open(path, 'r', encoding='utf-8') as src:
            with open('sample.txt', 'w') as dst:
                num_total = 0
                for line in src:
                    AnonID, Query, QueryTime = line.split('\t')[:3]

                    if AnonID == 'AnonID':
                        continue

                    if num_total < num_records:
                        tidy = self.trim(Query)
                        if tidy != '':
                            Query = self.remove_stop_words(tidy)
                            Query = self.porter_stemming(Query)
                            if Query != '':
                                dst.write('{}\t{}\t{}\n'.format(AnonID, Query, QueryTime))
                                num_total += 1

    def trim(self, string):
        return re.sub(r'\W', ' ', string)

    def remove_stop_words(self, string):
        words = string.split()
        return ' '.join([w for w in words if w not in self.stop])

    def porter_stemming(self, string):
        result = [self.porter.stem(word, 0, len(word) - 1) for word in string.split()]
        return ' '.join(result)


if __name__ == '__main__':
    p = Processor('AOL-user-ct-collection/user-ct-test-collection-01.txt', 1000)
