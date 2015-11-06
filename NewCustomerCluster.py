__author__ = 'Kyo'

import csv
import glob

from collections import defaultdict

def load_result_from_csv(filePath):
    user_score_dict = defaultdict(list) # each value in each column is appended to a list
    with open(filePath) as f:
        reader = csv.DictReader(f) # read rows into a dictionary format
        for row in reader: # read a row as {column1: value1, column2: value2,...}
            for (k,v) in row.items(): # go over each column name and value
                 user_score_dict[k].append(v) # append the value into the appropriate list based on column name k
    user_score_dict.pop('K\users')
    return user_score_dict

def clustering(path, user_score_dict, threshold):
    clusters = dict()
    users = user_score_dict.keys()
    users = map(int, users)
    users.sort()

    for user in users:
        key = str(user)
        scores = map(float, user_score_dict[key])
        for score in scores:
            if score > threshold:
                clusterNumber = scores.index(score)
                if not clusters.keys().__contains__(clusterNumber):
                    clusters[clusterNumber] = list()
                clusters[clusterNumber].append(user)

    write_path = path.split(".csv")[0] + "_threshold_" + str(threshold) + ".csv"
    with open(write_path,"w") as wf:
        for i in range(len(clusters.keys())):
            wf.write("Cluster"+str(i+1)+":,")
            if clusters.__contains__(i+1):
                users_of_cluster = clusters[i+1]
                for j in range(len(users_of_cluster)):
                    wf.write(str(users_of_cluster[j]))
                    if j != len(users_of_cluster)-1:
                        wf.write(",")
                wf.write("\n")
            else:
                wf.write("")
                wf.write("\n")

class cluster:
    threshold = [0.005,0.01,0.02,0.03]
    for file in glob.glob("./NewClusterResult/H_*.csv"):
        for value in threshold:
            user_score_dict = load_result_from_csv(file)
            clustering(file, user_score_dict, value)
            print file