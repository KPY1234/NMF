__author__ = 'kyo'

import csv
from collections import defaultdict

def load_matrix(matrix_path):
    columns = defaultdict(list)
    users_pattern = dict()
    begin = 1

    with open(matrix_path) as f:
        print "Loading the matrix.csv file (" + matrix_path + "), please wait.............."
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
                if v != '0':
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

def get_clusters_index(users_pattern, cluster_result):

    print "Get each cluster's index............................"
    clusters_index = dict()
    clusters_users_count = dict()
    clusters_users_patterns = dict()
    patterns_users_count = dict()

    print "Get each cluster's users count and patterns......................"
    for cluster in cluster_result:
        clusters_users_count[cluster] = len(cluster_result[cluster])
        clusters_users_patterns[cluster] = list()
        for user in cluster_result[cluster]:
            for pattern in users_pattern[user]:
                if str(pattern.keys()) in clusters_users_patterns[cluster]:
                    patterns_users_count[str(pattern.keys())] += 1
                else:
                    clusters_users_patterns[cluster].append(str(pattern.keys()))
                    patterns_users_count[str(pattern.keys())] = 0
        clusters_index[cluster] = 0
        for users_count in patterns_users_count:
            clusters_index[cluster] += float(patterns_users_count[users_count]) / (clusters_users_count[cluster] * len(
                clusters_users_patterns[cluster]))
    return clusters_index

class Evaluate:

    matrix_path = "D:\Python\workspacePy\matrix.csv"
    users_pattern = load_matrix(matrix_path)

    K = [3,4,5,8,9,10]
    Step = [400,500,600]
    Alpha = [0.0001,0.0002,0.0003]
    Beta = [0.01, 0.015, 0.02]
    for k in K:
        for step in Step:
            for alpha in Alpha:
                for beta in Beta:
                    result_path = "D:\Python\workspacePy\NMF\Results\Clusters_K" + k + "_steps" + step + "_alpha" + alpha + "_beta" + beta + ".csv"
                    cluster_result = load_cluster_result(result_path)
                    clusters_index = get_clusters_index(users_pattern, cluster_result)

    # clusters_top10_patterns = find_clusters_top10_patterns(cluster_result, users_pattern)



