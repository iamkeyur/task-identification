from datetime import datetime


class TimeSplitter:

    def __init__(self, path):
        self.split(path)

    def parse(self, date_string):
        return datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')

    def diff(self, t1, t2):
        return self.parse(t1) - self.parse(t2)

    def split(self, path):

        session = dict()
        task = dict()

        with open(path, 'r', encoding='utf-8') as input:

            current_user = ''

            for line in input:
                AnonID, Query, QueryTime = line[:-1].split('\t')

                if AnonID != current_user:
                    current_user = AnonID
                    session[AnonID] = []

                session[AnonID].append((Query, QueryTime))

        for user_id in session:
            previous_time = '2006-01-01 00:00:00'
            for query_id in range(len(session[user_id]) - 1):
                query = session[user_id][query_id][0]
                query_time = session[user_id][query_id][1]
                if query_id > 0:
                    previous_time = session[user_id][query_id - 1][1]

                diff = self.diff(query_time, previous_time)

                # print(query)
                if abs(diff).seconds >= 26 * 60:
                    print('-' * 30)


if __name__ == '__main__':
    s = TimeSplitter('sample.txt')