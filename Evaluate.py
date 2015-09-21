__author__ = 'kyo'

import csv
from collections import defaultdict
import CustomerCluster

def load_matrix(matrix_path):
    columns = defaultdict(list)
    users = list()
    users_pattern = dict()
    begin = 1

    with open(matrix_path) as f:

        print "Loading the matrix.csv file, please wait..............."
        reader = csv.DictReader(f)
        for row in reader:
            if begin:
                begin = 0
                users = row.keys()
                users.remove('patterns\users')
            for (k,v) in row.items():
                columns[k].append(v)
        patterns = columns['patterns\users']

        print "Transform to the user pattern, please wait..............."
        for user in range(len(users)):
            users_pattern[users.__getitem__(user)] = list()
            for idx in range(len(patterns)):
                pattern_value = int(columns[users.__getitem__(user)].__getitem__(idx))
                if pattern_value != 0:
                    users_pattern[users.__getitem__(user)].append({patterns.__getitem__(idx): pattern_value})
    return users_pattern

def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z

def merge_two_list(x, y):
    x = x.set(x + y)
    return x

class evaluate:

    matrix_path = "K:\workspacePy\ItemRecommender\matrix.csv"
    users_pattern = load_matrix(matrix_path)



