__author__ = 'kyo'

import csv
from collections import defaultdict

def load_matrix(matrix_path):
    columns = defaultdict(list)
    users_pattern = dict()
    begin = 1

    with open(matrix_path) as f:
        print "Loading the matrix.csv file, please wait: " + matrix_path
        reader = csv.DictReader(f)
        for row in reader:
            if begin:
                begin = 0
                users = row.keys()
                users.remove('patterns\users')
                for user in users:
                    users_pattern[user] = list()
            for (k,v) in row.items():
                if k == 'patterns\users':
                    continue
                if v != 0:
                    columns[k].append(v)
                    users_pattern[k].append({row['patterns\users']: v})
    return users_pattern

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

def find_clusters_top10_patterns(cluster_result, users_pattern):

    print "Find each cluster's top 10 patterns........................."
    cluster_top10_patterns = dict()

    for cluster in cluster_result:
        cluster_top10_patterns[cluster] = list()
        cluster_users = cluster_result[cluster]
        for cluster_user in cluster_users:
            # cluster_top10_patterns[cluster] = merge_list(cluster_top10_patterns[cluster], users_pattern[cluster_user].keys())
            print cluster_user
    return cluster_top10_patterns

def merge_list(a, b):
    c = list(set(a).union(set(b)))
    return c

class evaluate:

    matrix_path = "D:\Python\workspacePy\matrix2.csv"
    users_pattern = load_matrix(matrix_path)

    result_path = "D:\Python\workspacePy\NMF\Results\Clusters_K3_steps400_alpha0.0001_beta0.01.csv"
    cluster_result = load_cluster_result(result_path)

    cluster_patterns = find_clusters_top10_patterns(cluster_result, users_pattern)



