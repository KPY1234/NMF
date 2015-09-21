__author__ = 'User'

import csv
import heapq
import glob

from collections import defaultdict

def load_Q_matrix_from_csv(filePath):
     user_score_dict = defaultdict(list) # each value in each column is appended to a list
     with open(filePath) as f:
         reader = csv.DictReader(f) # read rows into a dictionary format
         for row in reader: # read a row as {column1: value1, column2: value2,...}
             # print row
             for (k,v) in row.items(): # go over each column name and value
                 # print row.items()
                 user_score_dict[k].append(v) # append the value into the appropriate list
                                 # based on column name k

     user_score_dict.pop('K\users')
     # print(user_score_dict['3'])
     # print(user_score_dict['6'])
     # print(user_score_dict['8'])

     return user_score_dict


def clustering(path, user_score_dict):
    clusters = dict()
    users = user_score_dict.keys()
    users = map(int, users)
    users.sort()

    for user in users:
        key = str(user)
        scores = map(float, user_score_dict[key])
        total_score = sum(scores)

        two_largest = heapq.nlargest(2, scores)

        max_score = two_largest[0]
        second_score = two_largest[1]

        max_score_index = 0
        second_score_index = -1

        if(max_score>(total_score/2)):
            max_score_index = scores.index(max_score)
        else:
            max_score_index = scores.index(max_score)
            second_score_index = scores.index(second_score)

        # print key+"\t"+str(scores)+"\t"+str(total_score)+"\t"+str(max_score_index)

        if(second_score_index == -1):
            if (clusters.__contains__(max_score_index+1)):
                users_of_cluster = clusters[max_score_index+1]
                users_of_cluster.append(user)
            else:
                users_of_cluster = list()
                users_of_cluster.append(user)
                clusters[max_score_index+1] = users_of_cluster
            print "user "+str(user)+" cluster:"+str(max_score_index)
        else:
            if (clusters.__contains__(max_score_index+1)):
                users_of_cluster = clusters[max_score_index+1]
                users_of_cluster.append(user)
            else:
                users_of_cluster = list()
                users_of_cluster.append(user)
                clusters[max_score_index+1] = users_of_cluster

            if (clusters.__contains__(second_score_index+1)):
                users_of_cluster = clusters[second_score_index+1]
                users_of_cluster.append(user)
            else:
                users_of_cluster = list()
                users_of_cluster.append(user)
                clusters[second_score_index+1] = users_of_cluster


            print "user "+str(user)+" cluster:"+str(max_score_index)+"\t"+str(second_score_index)


    write_path = path.replace("Q_matrix", "Clusters")
    # print write_path

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

    # print clusters


class cluster:

    for file in glob.glob("./Results/Q_matrix_*.csv"):
        user_score_dict = load_Q_matrix_from_csv(file)
        clustering(file, user_score_dict)
        print file

