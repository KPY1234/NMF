__author__ = 'kyo'

import csv
from collections import defaultdict

def load_matrix(matrix_path):
    columns = defaultdict(list)
    users = list()
    users_pattern = dict()
    patterns_count = dict()
    begin = 1

    with open(matrix_path) as f:

        print "Loading the matrix.csv file, please wait: " + matrix_path
        reader = csv.DictReader(f)
        for row in reader:
            if begin:
                begin = 0
                users = row.keys()
                users.remove('patterns\users')
            for (k,v) in row.items():
                columns[k].append(v)
        patterns = columns['patterns\users']

        print "Get the user's patterns, please wait..............."
        for user in range(len(users)):
            users_pattern[users.__getitem__(user)] = list()
            for pattern in range(len(patterns)):
                pattern_value = int(columns[users.__getitem__(user)].__getitem__(pattern))
                if pattern_value != 0:
                    users_pattern[users.__getitem__(user)].append({patterns.__getitem__(pattern): pattern_value})

        print "Get the patterns_count, please wait..............."
        for pattern in range(len(patterns)):
            for user in range(len(users)):
                users_pattern_list =  users_pattern[users.__getitem__(user)]
            patterns_count[patterns.__getitem__(pattern)] = sum(users_pattern_list)

    return users_pattern, patterns_count

def load_cluster_result(result_path):

    print "Loading the cluster resulte: " + result_path
    cluster_result = dict()
    idx = 1
    with open(result_path, 'rt') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in reader:
            line = ', '.join(row)
            cluster_result[idx] = line.split(',')[1:]
            idx += 1
    return cluster_result

def find_cluster_patterns(cluster_result, users_pattern):

    print "Find each cluster's patterns........................."
    cluster_patterns = dict()
    for key in cluster_result.keys():
        users = cluster_result[key]
        users = users.split(',')
        for user in range(len(users)):
            print user

    return cluster_patterns

class evaluate:

    matrix_path = "K:\workspacePy\ItemRecommender\matrix2.csv"
    users_pattern = load_matrix(matrix_path)
    result_path = "K:\workspacePy\NMF\Results\Clusters_K3_steps400_alpha0.0001_beta0.01.csv"
    cluster_result = load_cluster_result(result_path)
    cluster_patterns = find_cluster_patterns(cluster_result, users_pattern)



