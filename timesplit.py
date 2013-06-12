from datetime import datetime


class TimeSplitter:

    def __init__(self, path, time_gap=26):
        self.time_gap = time_gap

    def parse(self, date_string):
        return datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')

    def diff(self, t1, t2):
        return self.parse(t1) - self.parse(t2)

    def split(self, path):

        session = dict()
        order = []

        with open(path, 'r', encoding='utf-8') as input:

            current_user = ''

            for line in input:
                AnonID, Query, QueryTime = line[:-1].split('\t')

                if AnonID != current_user:
                    current_user = AnonID
                    order.append(AnonID)
                    session[AnonID] = []

                session[AnonID].append((Query, QueryTime))

        doc_id = 0

        order = ['2178', '3769']

        for user_id in order:

            with open('/Users/susen/Projects/cs290n/intermediate/{}.log'.format(user_id)) as log:
                for query_id in range(len(session[user_id])):
                    query = session[user_id][query_id][0]
                    query_time = session[user_id][query_id][1]
                    if query_id < len(session[user_id]) - 1:
                        next_time = session[user_id][query_id + 1][1]

                    log.write(query + '\n')

                    diff = self.diff(query_time, next_time)
                    if abs(diff).seconds >= self.time_gap * 60:
                        log.write('#\n')

                    doc_id += 1


if __name__ == '__main__':
    s = TimeSplitter('sample.txt')