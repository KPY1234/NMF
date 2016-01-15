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

    for cluster in cluster_result:
        clusters_index[cluster] = 0
        clusters_users_patterns = dict()
        cluster_top_patterns = ""
        user_list = ""
        for user in cluster_result[cluster]:
            user_list += user
        user_list = user_list.replace("\\n", "").split(" ")
        for user in user_list:
            for pattern in users_pattern[user]:
                for pattern_key in pattern.keys():
                    if not clusters_users_patterns.__contains__(pattern_key):
                        clusters_users_patterns[pattern_key] = 0
                    clusters_users_patterns[pattern_key] += int(pattern[pattern_key])
        for patterns in clusters_users_patterns:
            if clusters_users_patterns[patterns] == max(clusters_users_patterns.values()):
                cluster_top_patterns = patterns
        for user in user_list:
            for pattern in users_pattern[user]:
                if pattern.keys == cluster_top_patterns:
                    clusters_index[cluster] += pattern.values / (users_pattern[user].__len__() - 1) / user_list.__len__()
                    break
        print clusters_index[cluster]
    return clusters_index

class Evaluate:

    matrix_path = "./DataSet/matrix.csv"
    users_pattern = load_matrix(matrix_path)

    for file in glob.glob("./NewClusterResult/H_*_refined_refined_*.csv"):
        result_path = file
        if os.path.exists(result_path):
            cluster_result = load_cluster_result(result_path)
            clusters_index = get_clusters_index(users_pattern, cluster_result)
            write_path = "./Result/" + file.split(".csv")[0] + "_EvaluateResultRefined.csv"
            print "Write the evaluate result to file:" + write_path
            with open(write_path, "w") as wf:
                for cluster in clusters_index:
                    wf.write("Cluster"+str(cluster)+":,")
                    wf.write(str(clusters_index[cluster]) + ",")
                    wf.write(str(len(cluster_result[cluster])))
                    wf.write("\n")