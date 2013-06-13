from distance import Lexical, Semantic
import copy


class Cluster:
    def __init__(self, sequence, l, s, start=0, threshold=0.2, t=0.5, b=5):
        self.lexical = l  # Lexical()
        self.semantic = s  # Semantic('/Users/susen/Projects/cs290n/intermediate/index.txt')
        self.sequence = sequence
        self.b = b
        self.t = t
        self.threshold = threshold
        self.start = start
        self.graph = {}
        self.prepare()

    def prepare(self):
        for i in range(len(self.sequence)):
            self.graph[i] = []
            for j in range(i+1, len(self.sequence)):
                self.graph[i].append(j)

    def wcc(self):
        self.result = copy.deepcopy(self.graph)
        for i in self.graph:
            for j in self.graph[i]:
                s1, s2 = self.sequence[i], self.sequence[j]
                content = self.lexical.content_distance(s1, s2)
                if content < self.t:
                    similarity = content
                else:
                    semantic = self.semantic.semantic_distance_wiki(s1, s2)
                    # print(s1, '/', s2, 'semantic=', semantic)
                    similarity = min(self.b * semantic, content)

                # print(i, j, s1, '/', s2, similarity)

                if 1 - similarity < self.threshold:
                    self.result[i].remove(j)

    def generate_cluster(self, graph, time_only=False):

        if time_only:
            all = set([i+self.start for i in range(len(self.sequence))])
            return [all]

        cluster = []
        result = [{'cluster': set([i] + graph[i]), 'visited': False} for i in graph]
        # print(result)

        all_visited = False
        while not all_visited:
            c = set()
            all_visited = True
            for i in range(len(result)):
                ci = result[i]
                if not ci['visited']:
                    all_visited = False
                    c = c.union(ci['cluster'])
                    result[i]['visited'] = True
                    for j in range(i+1, len(result)):
                        cj = result[j]
                        if ci['cluster'].intersection(cj['cluster']) != set() and not cj['visited']:
                            c = c.union(cj['cluster'])
                            result[j]['visited'] = True
                    break

            if c != set():
                cluster.append(c)

        # print(cluster)

        post_cluster = []
        # post process
        rest = set([i for i in range(len(self.sequence))])
        for c in cluster:
            if len(c) > 1:
                post_cluster.append(c)

        for c in post_cluster:
            rest = rest.difference(c)

        if rest != set():
            post_cluster.append(rest)

        final_cluster = []
        for c in post_cluster:
            final_cluster.append(set())
            for i in c:
                final_cluster[-1].add(i + self.start)

        return final_cluster


if __name__ == '__main__':

    s = ['door viewer',
         'door viewer',
         'door viewer',
         'door viewer',
         'peep hole',
         'peephol',
         'home depot',
         'sear',
         'walmart',
         'target',
         'door viewer',
         'birthdai cake',
         'birthdai cake',
         'birthdai cake',
         'birthdai cake',
         'custom birthdai cake atlanta ga']

    c = Cluster(s)
    c.wcc()
    c.generate_cluster(c.result)