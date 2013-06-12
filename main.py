from timesplit import TimeSplitter
from cluster import Cluster
from distance import Lexical, Semantic


def do_exp(path, start=0):
    with open(path, 'r', encoding='utf-8') as log:
        time_slice = log.read().split('#\n')
        # print(time_slice)
        sequence = [s[:-1].split('\n') for s in time_slice]
        # print(sequence)

    cluster = []
    lexical = Lexical()
    semantic = Semantic('/Users/susen/Projects/cs290n/intermediate/index.txt')
    offset = start

    for s in sequence:
        c = Cluster(s, lexical, semantic, start=offset)
        c.wcc()
        cluster += c.generate_cluster(c.result)
        offset += len(s)

    return cluster


def read_standard(path):
    with open(path, 'r', encoding='utf-8') as standard:
        l = standard.read().split('\n')

    return [set([int(j) for j in i.split(',')]) for i in l]


def is_together(cluster, s):
    for c in cluster:
        if s.issubset(c):
            return True

    return False


def get_score(predicted, standard, r):
    # r[0] lower bound, r[1] upper bound
    TP, FP, FN, TN = 0, 0, 0, 0
    all = [i for i in range(r[0], r[1]+1)]

    for i in range(len(all)):
        for j in range(i+1, len(all)):
            pair = set([all[i], all[j]])
            #print(pair)
            x = is_together(standard, pair)
            y = is_together(predicted, pair)
            if x and y:
                TP += 1
            if x and not y:
                FN += 1
            if not x and y:
                FP += 1
            if not x and not y:
                TN += 1

    return TP, FP, FN, TN


def precision(TP, FP, FN, TN):
    return TP / (TP + FP) if TP != 0 else 0


def recall(TP, FP, FN, TN):
    return TP / (TP + FN) if TP != 0 else 0


def F1_score(TP, FP, FN, TN):
    P = precision(TP, FP, FN, TN)
    R = recall(TP, FP, FN, TN)
    print('Precision=', P, ', Recall=', R)
    return 2 * P * R / (P + R)


def RI(TP, FP, FN, TN):
    return (TP + TN) / (TP + FP + FN + TN)


def JI(TP, FP, FN, TN):
    return TP / (FP + TP + FN)


if __name__ == '__main__':
    s = TimeSplitter('sample.txt', time_gap=26)  # set time session gap as 26 minutes

    print('User #2178')
    predicted = do_exp('/Users/susen/Projects/cs290n/intermediate/2178.log', start=205)
    standard = read_standard('/Users/susen/Projects/cs290n/intermediate/2178.labeled.txt')
    TP, FP, FN, TN = get_score(predicted, standard, (205, 324))
    # print(standard)
    # print(predicted)
    print(TP, FP, FN, TN)
    print('F1 Score =', F1_score(TP, FP, FN, TN))
    print('Rand Index =', RI(TP, FP, FN, TN))
    print('Jaccard Index = ', JI(TP, FP, FN, TN))

    print('\nUser #3796:')
    predicted = do_exp('/Users/susen/Projects/cs290n/intermediate/3769.log', start=1506)
    standard = read_standard('/Users/susen/Projects/cs290n/intermediate/3769.labeled.txt')
    TP, FP, FN, TN = get_score(predicted, standard, (1506, 1575))
    # print(standard)
    # print(predicted)
    print(TP, FP, FN, TN)
    print('F1 Score =', F1_score(TP, FP, FN, TN))
    print('Rand Index =', RI(TP, FP, FN, TN))
    print('Jaccard Index = ', JI(TP, FP, FN, TN))