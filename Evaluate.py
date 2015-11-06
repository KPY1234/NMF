__author__ = 'kyo'

import csv
import os
import glob
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

    clusters_index = dict()
    clusters_users_count = dict()
    clusters_users_patterns = dict()

    for cluster in cluster_result:
        patterns_users_count = dict()
        if cluster_result[cluster][0] == '':
            continue
        clusters_users_count[cluster] = len(cluster_result[cluster])
        clusters_users_patterns[cluster] = list()
        print "Get cluster:" + str(cluster) + " users count and patterns..."
        for user in cluster_result[cluster]:
            for pattern in users_pattern[user]:
                if str(pattern.keys()) in clusters_users_patterns[cluster]:
                    patterns_users_count[str(pattern.keys())] += 1
                else:
                    clusters_users_patterns[cluster].append(str(pattern.keys()))
                    patterns_users_count[str(pattern.keys())] = 1
        clusters_index[cluster] = 0
        print "Get cluster:" + str(cluster) + " index..."
        for users_count in patterns_users_count:
            clusters_index[cluster] += float(patterns_users_count[users_count]) / (float(clusters_users_count[cluster] * len(
                clusters_users_patterns[cluster])))
        print clusters_index[cluster]
    return clusters_index

class Evaluate:

    matrix_path = "./DataSet/matrix.csv"
    users_pattern = load_matrix(matrix_path)

    for file in glob.glob("./NewClusterResult/H_*_threshold_*.csv"):
        result_path = file
        if os.path.exists(result_path):
            cluster_result = load_cluster_result(result_path)
            clusters_index = get_clusters_index(users_pattern, cluster_result)
            write_path = file.split(".csv")[0] + "_EvaluateResult.csv"
            print "Write the evaluate result to file:" + write_path
            with open(write_path,"w") as wf:
                for cluster in clusters_index:
                    wf.write("Cluster"+str(cluster)+":,")
                    wf.write(str(clusters_index[cluster]) + ",")
                    wf.write(str(len(cluster_result[cluster])))
                    wf.write("\n")