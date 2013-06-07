def trigram(s):
    tri = set()

    if len(s) <= 3:
        tri.add(s)
    else:
        for i in range(len(s) - 2):
            tri.add(s[i:i+3])

    return tri


def jaccard(s1, s2):
    c1 = trigram(s1)
    c2 = trigram(s2)

    return 1 - len(c1.intersection(c2)) / len(c1.union(c2))


def levenshtein(seq1, seq2):
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

    return this_row[len(seq2) - 1] / (len(seq1) + len(seq2)) * 2


def content_distance(s1, s2):
    return (jaccard(s1, s2) + levenshtein(s1, s2)) / 2


if __name__ == '__main__':
    s1 = 'honda accord fuel addit check engin light'
    s2 = 'honda accord check engin light pa emiss'

    print(content_distance(s1, s2))
