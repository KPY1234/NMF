__author__ = 'Kao & Kyo'
import numpy
import pickle
import time
import os

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

    if not os.path.exists('./Results'):
        os.makedirs('./Results')

    ## write patterns\users matrix
    filename = "./Results/NMF_matrix_K"+str(K)+"_steps"+str(steps)+"_alpha"+str(alpha)+"_beta"+str(beta)+".csv"
    with open(filename,"w") as wf:
        wf.write("patterns\users,")
        for i in range(len(users)):
            wf.write(str(users[i]))
            if i != len(users)-1:
                wf.write(",")
        wf.write("\n")

        for i in range(len(nR)):
            wf.write(str(patterns[i]).replace(',','-')+",")
            for j in range(len(nR[i])):
                wf.write(str(nR[i][j]))
                if j != len(nR[i])-1:
                    wf.write(",")
            wf.write("\n")

    ## write patterns\K matrix
    filename = "./Results/P_matrix_K"+str(K)+"_steps"+str(steps)+"_alpha"+str(alpha)+"_beta"+str(beta)+".csv"
    with open(filename,"w") as wf:
        wf.write("patterns\K,")
        for i in range(K):
            wf.write(str(i))
            if i != K-1:
                wf.write(",")
        wf.write("\n")

        for i in range(len(nP)):
            wf.write(str(patterns[i]).replace(',','-')+",")
            for j in range(len(nP[i])):
                wf.write(str(nP[i][j]))
                if j != len(nP[i])-1:
                    wf.write(",")
            wf.write("\n")


    ## write K\users matrix
    filename = "./Results/Q_matrix_K"+str(K)+"_steps"+str(steps)+"_alpha"+str(alpha)+"_beta"+str(beta)+".csv"
    with open(filename,"w") as wf:
        wf.write("K\users,")
        for i in range(len(users)):
            wf.write(str(users[i]))
            if i != len(users)-1:
                wf.write(",")
        wf.write("\n")

        for i in range(len(nQ.T)):
            wf.write(str(i)+",")
            for j in range(len(nQ.T[i])):
                wf.write(str(nQ.T[i][j]))
                if j != len(nQ.T[i])-1:
                    wf.write(",")
            wf.write("\n")
    return nQ.T


def matrix_factorisation(R, P, Q, K, steps, alpha, beta):

    print "runing the nmf algorithm, please wait..."

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

    filename = "./Results/Clusters_K"+str(K)+"_steps"+str(steps)+"_alpha"+str(alpha)+"_beta"+str(beta)+".csv"

    clusters = dict()
    for i in range(len(Q[0])):
        user = users[i]
        columnList = Q[:,i]
        clusterNum = columnList.tolist().index(max(columnList))+1
        # print str(user)+"\t"+str(columnList)+"\t"+str(clusterNum)
        if clusters.__contains__(clusterNum):
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

    with open('./pkls/filter_users.pkl') as rf:

        filter_users = pickle.load(rf)
    with open('./pkls/patterns.pkl') as rf:
        patterns = pickle.load(rf)
    with open('./pkls/normal_matrix.pkl') as rf:
        normal_matrix = pickle.load(rf)


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
                    Q = nmf_imp(filter_users, patterns, normal_matrix, i, j, k, l)
                    cluster(filter_users, Q, i, j, k, l)
