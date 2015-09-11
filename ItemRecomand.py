__author__ = 'Kao & Kyo'
import csv
import numpy
import math


def load_csv(filePath):
     user_dict = dict()   # record every user dealed information
     with open(filePath, 'rt') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            line = ', '.join(row)
            user = int(line.split(',')[1])
            if (user_dict.__contains__(user)):
                lines = user_dict[user]
                lines.append(line)
            else:
                lines = list()
                lines.append(line)
                user_dict[user] = lines
     # print(d['6'])
     return user_dict


def user_transaction_mapping(user_dict):
    user_transaction_dict = dict()
    keys = sorted(user_dict.keys())
    for key in keys:  # record every user transaction information in hierarchy
        lines = user_dict[key]
        time_dict = dict()

        for line in lines:
            item = int(line.split(',')[0])
            time = int(line.split(',')[2])
            if (time_dict.__contains__(time)):
                items = time_dict[time]
                items.append(item)
            else:
                items = list()
                items.append(item)
                time_dict[time] = items

        time_keys = time_dict.keys()
        for time_key in time_keys:
            items = time_dict[time_key]
            items.sort()
            time_dict[time_key] = set(items)

        user_transaction_dict[key] = time_dict

    # print(user_transaction_dict[8])
    return user_transaction_dict


def transToUserPatternDict(user_transaction_dict):

    print ("transfer to dictionary of user and pattern, please wait...")

    user_pattern_dic = dict();
    patterns = list()

    users = user_transaction_dict.keys()
    usercount = 0
    for user in users:
        usercount+=1
        # print(user)
        user_transactions = user_transaction_dict[user]
        #print(user_transactions)
        deal_times = user_transactions.keys()
        deal_times.sort()
        for i in range(len(deal_times)-1):
            deal_time1 = deal_times[i]
            deal_time2 = deal_times[i+1]
            items1 = user_transactions[deal_time1]
            items2 = user_transactions[deal_time2]
            one_user_patterns = getAllPatterns(items1, items2, patterns)
            for one_user_pattern in one_user_patterns:
                if (user_pattern_dic.__contains__(user)):
                    if(user_pattern_dic[user].__contains__(one_user_pattern)):
                        count = user_pattern_dic[user][one_user_pattern]
                        count+=1
                        user_pattern_dic[user][one_user_pattern] = count

                    else:
                        pattern_count_dic = user_pattern_dic[user]
                        pattern_count_dic[one_user_pattern] = 1
                        user_pattern_dic[user] = pattern_count_dic
                else:
                    pattern_count_dic = dict()
                    pattern_count_dic[one_user_pattern] = 1
                    user_pattern_dic[user] = pattern_count_dic

        # if(usercount%1000 == 0):
        #     print (usercount)
    # print user_pattern_dic[8]

    return (user_pattern_dic, patterns)

def getAllPatterns(items1, items2, patterns):
    localPatterns = list()
    for item1 in items1:
        for item2 in items2:
            pattern = (item1, item2)
            localPatterns.append(pattern)
            # print(pattern)
            if(not patterns.__contains__(pattern)):
                patterns.append(pattern)
    return localPatterns


def transToMatrix(users, user_pattern_dic, patterns):

    print ("transfer to matrix, please wait...")

    patterns.sort()

    rows = len(patterns)
    columns = len(users)

    user_pattern_matrix = [[0 for x in range(columns)] for y in range(rows)]

    column = 0
    for user in users:
        # print(user)
        row = 0
        for pattern in patterns:
            # print(pattern)
            if (user_pattern_dic.__contains__(user)):
                if(user_pattern_dic[user].__contains__(pattern)):
                    count = user_pattern_dic[user][pattern]
                    user_pattern_matrix[row][column] = count
            row+=1
        column+=1

    with open("./matrix.csv","w") as wf:
        wf.write("patterns\users,")
        for i in range(len(users)):
            wf.write(str(users[i]))
            if(i != len(users)-1):
                wf.write(",")
        wf.write("\n")

        for i in range(len(user_pattern_matrix)):
            wf.write(str(patterns[i]).replace(',','-')+",")
            for j in range(len(user_pattern_matrix[i])):
                wf.write(str(user_pattern_matrix[i][j]))
                if(j != len(user_pattern_matrix[i])-1):
                    wf.write(",")
            wf.write("\n")

    return user_pattern_matrix


def normalizeMatrix(users, user_pattern_matrix, patterns):

    print ("normalize the matrix, please wait...")

    for i in range(len(user_pattern_matrix[0])):
        user_pattern_counts = [row[i] for row in user_pattern_matrix]
        user_count_sum = sum(user_pattern_counts)
        if(user_count_sum == 0):
            continue

        for j in range(len(user_pattern_counts)):
            count = user_pattern_counts[j]
            count = 1.0*count/user_count_sum * 1000
            count = round(count);
            # user_pattern_counts[j] = count
            user_pattern_matrix[j][i] = count

    with open("./normal_matrix.csv","w") as wf:
        wf.write("patterns\users,")
        for i in range(len(users)):
            wf.write(str(users[i]))
            if(i != len(users)-1):
                wf.write(",")
        wf.write("\n")

        for i in range(len(user_pattern_matrix)):
            wf.write(str(patterns[i]).replace(',','-')+",")
            for j in range(len(user_pattern_matrix[i])):
                wf.write(str(user_pattern_matrix[i][j]))
                if(j != len(user_pattern_matrix[i])-1):
                    wf.write(",")
            wf.write("\n")

    return user_pattern_matrix

def nmf_imp(users, patterns, normal_matrix, K, steps, alpha, beta):
    R = numpy.array(normal_matrix)
    N = len(R)
    M = len(R[0])

    P = numpy.random.rand(N,K)
    Q = numpy.random.rand(M,K)

    for i in range(len(P)):
        for j in range(len(P[i])):
            P[i][j] = round(P[i][j], 5)

    for i in range(len(Q)):
        for j in range(len(Q[i])):
            Q[i][j] = round(Q[i][j], 5)

    nP, nQ = matrix_factorisation(R, P, Q, K, steps, alpha, beta)
    nR = numpy.dot(nP, nQ.T)

    ## write patterns\users matrix
    filename = "./NMF_matrix_K"+str(K)+"_steps"+str(steps)+"_alpha"+str(alpha)+"_beta"+str(beta)+".csv"
    with open(filename,"w") as wf:
        wf.write("patterns\users,")
        for i in range(len(users)):
            wf.write(str(users[i]))
            if(i != len(users)-1):
                wf.write(",")
        wf.write("\n")

        for i in range(len(nR)):
            wf.write(str(patterns[i]).replace(',','-')+",")
            for j in range(len(nR[i])):
                wf.write(str(nR[i][j]))
                if(j != len(nR[i])-1):
                    wf.write(",")
            wf.write("\n")

    ## write patterns\K matrix
    filename = "./P_matrix_K"+str(K)+"_steps"+str(steps)+"_alpha"+str(alpha)+"_beta"+str(beta)+".csv"
    with open(filename,"w") as wf:
        wf.write("patterns\K,")
        for i in range(K):
            wf.write(str(i))
            if(i != K-1):
                wf.write(",")
        wf.write("\n")

        for i in range(len(nP)):
            wf.write(str(patterns[i]).replace(',','-')+",")
            for j in range(len(nP[i])):
                wf.write(str(nP[i][j]))
                if(j != len(nP[i])-1):
                    wf.write(",")
            wf.write("\n")


    ## write K\users matrix
    filename = "./Q_matrix_K"+str(K)+"_steps"+str(steps)+"_alpha"+str(alpha)+"_beta"+str(beta)+".csv"
    with open(filename,"w") as wf:
        wf.write("K\users,")
        for i in range(len(users)):
            wf.write(str(users[i]))
            if(i != len(users)-1):
                wf.write(",")
        wf.write("\n")

        for i in range(len(nQ.T)):
            wf.write(str(i)+",")
            for j in range(len(nQ.T[i])):
                wf.write(str(nQ.T[i][j]))
                if(j != len(nQ.T[i])-1):
                    wf.write(",")
            wf.write("\n")
    return nQ.T


def matrix_factorisation(R, P, Q, K, steps, alpha, beta):

    print("runing the nmf algorithm, please wait...")

    Q = Q.T
    for step in range(steps):
        print("step "+str(step))
        for i in range(len(R)):
            for j in range(len(R[i])):
                if R[i][j] > 0:
                    eij = R[i][j] - numpy.dot(P[i,:],Q[:,j])
                    for k in range(K):
                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                        Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
                        # print (str(Q[k][j])+"+"+str(alpha)+"*("+str(eij)+"*"+str(P[i][k]))
        eR = numpy.dot(P,Q)
        e = 0
        for i in range(len(R)):
            for j in range(len(R[i])):
                if R[i][j] > 0:
                    e = e + pow(R[i][j] - numpy.dot(P[i,:],Q[:,j]), 2)
                    for k in range(K):
                        e = e + (beta/2) * (pow(P[i][k],2) + pow(Q[k][j],2))
        if e < 0.001:
            break
    return P, Q.T


def cluster(users, Q, K, steps, alpha, beta):

    filename = "./Clusters_K"+str(K)+"_steps"+str(steps)+"_alpha"+str(alpha)+"_beta"+str(beta)+".csv"

    clusters = dict()
    for i in range(len(Q[0])):
        user = users[i]
        columnList = Q[:,i]
        clusterNum = columnList.tolist().index(max(columnList))+1
        # print str(user)+"\t"+str(columnList)+"\t"+str(clusterNum)
        if (clusters.__contains__(clusterNum)):
            users_of_cluster = clusters[clusterNum]
            users_of_cluster.append(user)
        else:
            users_of_cluster = list()
            users_of_cluster.append(user)
            clusters[clusterNum] = users_of_cluster

    with open(filename,"w") as wf:
        for i in range(K):

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
            # print (str(i+1)+"\t"+str(users_of_cluster))

class Module_data_mining:

    path = "./data.csv"
    d = load_csv(path)
    users = sorted(d.keys())
    trans_dic = user_transaction_mapping(d)

    user_pattern_dict, patterns = transToUserPatternDict(trans_dic)
    matrix = transToMatrix(users, user_pattern_dict, patterns)
    normal_matrix = normalizeMatrix(users, matrix, patterns)

    # K = 5   #cluster number
    # steps=500   #iteration number
    # alpha=0.0002    #gradient descent constant
    # beta=0.02   #0~0.02

    k_list = [8, 9, 10]
    steps_list = [500]
    alpha_list = [0.0001,0.0002,0.0003]
    beta_list = [0.015, 0.02]

    for i in k_list:
        for j in steps_list:
            for k in alpha_list:
                for l in beta_list:
                    Q = nmf_imp(users, patterns, normal_matrix, i, j, k, l)
                    cluster(users, Q, i, j, k, l)
