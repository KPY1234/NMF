import csv
import os
import glob
import operator
from collections import defaultdict

__author__ = 'kyo'

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
            for (k, v) in row.items():
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

def get_cluster_users(cluster_result):
    clusters_users = dict()
    for cluster in cluster_result:
        user_list = ""
        for user in cluster_result[cluster]:
            if user != " " and user != "" and user != "\n":
                    user_list += user
        clusters_users[cluster] = user_list.split(" ")
    return clusters_users

def get_clusters_index(users_pattern, cluster_result, top_pattern_number):
    clusters_top_n_patterns = dict()
    clusters_index = dict()
    for cluster in cluster_result:
        user_list = get_cluster_users(cluster_result)[cluster]
        clusters_users_patterns = dict()
        top_patterns = list()

        for user in user_list:
            for pattern in users_pattern[user]:
                for pattern_key in pattern.keys():
                    if not clusters_users_patterns.__contains__(pattern_key):
                        clusters_users_patterns[pattern_key] = 0
                    clusters_users_patterns[pattern_key] += int(pattern[pattern_key])

        sorted_clusters_users_patterns = sorted(clusters_users_patterns.items(), key=operator.itemgetter(1))

        for i in range(top_pattern_number):
            if (len(sorted_clusters_users_patterns) - i - 1) >= 0:
                top_patterns.append(sorted_clusters_users_patterns[len(sorted_clusters_users_patterns) - i - 1][0])

        top_patterns_users = dict()

        for top_pattern in top_patterns:
            top_patterns_users[top_pattern] = 0
            for user in user_list:
                for pattern in users_pattern[user]:
                    if pattern.keys()[0] == top_pattern:
                        top_patterns_users[top_pattern] += 1

        clusters_index[cluster] = 0.0

        if top_patterns.__len__() == top_pattern_number:
            for top_pattern in top_patterns_users:
                clusters_index[cluster] += float(top_patterns_users[top_pattern]) / user_list.__len__() / top_pattern_number
        else:
            clusters_index[cluster] = 1

        clusters_top_n_patterns[cluster] = top_patterns

    return clusters_index, clusters_top_n_patterns

# def get_pattern_rework(top_patterns, top_pattern_number):
#     rework_top_patterns
#
#     return rework_top_patterns

def get_cluster_dissimilar(clusters_top_n_patterns, cluster_users):
    user_cnt = 0.0
    clusters_top_n_patterns_cnt = 0.0
    top_pattern_dict = dict()
    tmp = 0.0
    for cluster in cluster_users:
        user_cnt += cluster_users[cluster].__len__()
        clusters_top_n_patterns_cnt += clusters_top_n_patterns[cluster].__len__()
        for pattern in clusters_top_n_patterns[cluster]:
            if pattern in top_pattern_dict.keys():
                top_pattern_dict[pattern].append(cluster)
            else:
                top_pattern_dict[pattern] = list()
                top_pattern_dict[pattern].append(cluster)
    for pattern in top_pattern_dict:
        if top_pattern_dict[pattern].__len__() > 1:
            total_pattern_users = 0.0
            for cluster in top_pattern_dict[pattern]:
                total_pattern_users += cluster_users[cluster].__len__()
            tmp += (top_pattern_dict[pattern].__len__()/clusters_top_n_patterns_cnt)*(total_pattern_users/user_cnt)
    cluster_dissimilar = 1 - tmp
    return cluster_dissimilar

def get_cluster_similarity(clusters_top_n_patterns):
    cluster_similarity = dict()
    cluster_num = float(clusters_top_n_patterns.__len__() - 1)
    for cluster in clusters_top_n_patterns:
        cnt = 0.0
        for patterns in clusters_top_n_patterns[cluster]:
            for c in clusters_top_n_patterns:
                if c != cluster:
                    for p in clusters_top_n_patterns[c]:
                        if p == patterns:
                            cnt += 1/float(clusters_top_n_patterns[cluster].__len__())
        cluster_similarity[cluster] = (cluster_num - cnt)/cluster_num
    return cluster_similarity

class Evaluate:

    top_pattern = {3, 5, 10, 15, 20}

    matrix_path = "./DataSet/matrix.csv"
    users_pattern = load_matrix(matrix_path)

    total_value = 0
    total_user = 0

    for top_pattern_number in top_pattern:
        for file in glob.glob("./NewClusterResult/H_*_1e-8_refined_cluster.csv"):
            result_path = file
            if os.path.exists(result_path):
                cluster_result = load_cluster_result(result_path)
                [clusters_index, clusters_top_n_patterns] = get_clusters_index(users_pattern, cluster_result,
                                                                               top_pattern_number)
                cluster_users = get_cluster_users(cluster_result)
                cluster_similarity = get_cluster_similarity(clusters_top_n_patterns)
                write_path = file.split(".csv")[
                                 0] + "_topPattern" + str(top_pattern_number) + "_EvaluateResultRefined.csv"
                print "Write the evaluate result to file:" + write_path
                with open(write_path, "w") as wf:
                    total_value = 0.
                    total_user = 0
                    sum_ns = 0.
                    for cluster in clusters_index:
                        wf.write("Cluster"+str(cluster)+":,")
                        wf.write(str(clusters_index[cluster]) + ",")
                        wf.write(str(len(cluster_users[cluster])) + ",")
                        for patterns in clusters_top_n_patterns[cluster]:
                            wf.write(str(patterns) + ",")
                        wf.write(str(cluster_similarity[cluster]) + ",")
                        total_value += clusters_index[cluster] * len(cluster_users[cluster])
                        total_user += len(cluster_users[cluster])
                        sum_ns += cluster_similarity[cluster]
                        wf.write("\n")
                    wf.write("EvaValue:" + "," + str(total_value/total_user))
                    ns_means = sum_ns/clusters_top_n_patterns.keys().__len__()
                    for num in range(clusters_top_n_patterns[clusters_top_n_patterns.keys()[1]].__len__()):
                        wf.write(",")
                    wf.write("," + "NonSimilarityMeans:" + "," + str(ns_means))
                    wf.write("\n" + ",")
                    for num in range(clusters_top_n_patterns[clusters_top_n_patterns.keys()[1]].__len__()):
                        wf.write(",")
                    wf.write("," + "Dissimilar:" + "," + str(get_cluster_dissimilar(clusters_top_n_patterns, cluster_users)))