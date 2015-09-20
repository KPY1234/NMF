__author__ = 'User'

import csv
import heapq
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


def clustering(user_score_dict):
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
            print "user "+str(user)+" cluster:"+str(max_score_index)
        else:
            print "user "+str(user)+" cluster:"+str(max_score_index)+"\t"+str(second_score_index)


    # print users


class cluster:

    path = "./Results/Q_matrix_K3_steps400_alpha0.0001_beta0.01.csv"
    user_score_dict = load_Q_matrix_from_csv(path)
    clustering(user_score_dict)