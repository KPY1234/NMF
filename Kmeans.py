__author__ = 'User'




from numpy import *
import csv
import time
# import matplotlib.pyplot as plt


# calculate Euclidean distance
def euclDistance(vector1, vector2):
    return sqrt(sum(power(vector2 - vector1, 2)))

# init centroids with random samples
def initCentroids(dataSet, k):
    numSamples, dim = dataSet.shape
    centroids = zeros((k, dim))
    for i in range(k):
        index = int(random.uniform(0, numSamples))
        centroids[i, :] = dataSet[index, :]
    return centroids

# k-means cluster
def kmeans(dataSet, k, max_iter=100000):
    num_samples = dataSet.shape[0]

    # first column stores which cluster this sample belongs to,
    # second column stores the distance between this sample and its centroid

    cluster_assignment = mat(zeros((num_samples, 2)))

    clusterChanged = True

    ## step 1: init centroids
    centroids = initCentroids(dataSet, k)

    iter = 0

    while clusterChanged:
        clusterChanged = False
        ## for each sample
        for i in xrange(num_samples):
            minDist  = 100000.0
            minIndex = 0
            ## for each centroid
            ## step 2: find the centroid who is closest
            for j in range(k):
                distance = euclDistance(centroids[j, :], dataSet[i, :])
                if distance < minDist:
                    minDist  = distance
                    minIndex = j

            ## step 3: update its cluster
            if cluster_assignment[i, 0] != minIndex:
                clusterChanged = True
                cluster_assignment[i, :] = minIndex, minDist**2

        ## step 4: update centroids
        for j in range(k):
            pointsInCluster = dataSet[nonzero(cluster_assignment[:, 0].A == j)[0]]
            centroids[j, :] = mean(pointsInCluster, axis = 0)

        iter+=1
        if iter == max_iter:
            break

    print 'Congratulations, cluster complete!'
    return centroids, cluster_assignment

# show your cluster only available with 2-D data
# def showCluster(dataSet, k, centroids, clusterAssment):
#     numSamples, dim = dataSet.shape
#     if dim != 2:
#         print "Sorry! I can not draw because the dimension of your data is not 2!"
#         return 1
#
#     mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']
#     if k > len(mark):
#         print "Sorry! Your k is too large! please contact Zouxy"
#         return 1
#
#     # draw all samples
#     for i in xrange(numSamples):
#         markIndex = int(clusterAssment[i, 0])
#         plt.plot(dataSet[i, 0], dataSet[i, 1], mark[markIndex])
#
#     mark = ['Dr', 'Db', 'Dg', 'Dk', '^b', '+b', 'sb', 'db', '<b', 'pb']
#     # draw the centroids
#     for i in range(k):
#         plt.plot(centroids[i, 0], centroids[i, 1], mark[i], markersize = 12)
#
#     plt.show()

def cluster_output(file_name, clusters):
     with open(file_name,"w") as wf:
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

class kmeans_class:
    ## step 1: load data
    print "step 1: load data..."

    f = csv.reader(open('./DataSet/normal_matrix.csv'))
    fields = f.next()
    dimension = len(fields)-1

    columns = zip(*f)
    columns.pop(0)

    dataSet = list()

    for i in xrange(len(columns)):

        values = map(float, columns[i])
        # print values
        dataSet.append(values)

    # step 2: clustering...
    print "step 2: clustering..."
    dataSet = mat(dataSet)


    list_k = [4,5,6,7,8]

    for i in xrange(len(list_k)):
        k = list_k[i]

        centroids, cluster_assignment = kmeans(dataSet, k)

        nums_samples = cluster_assignment.shape[0]

        dic = dict()

        for j in xrange(nums_samples):

            user = fields[j+1]
            cluster_num = cluster_assignment[j, 0]

            if cluster_num in dic:
                l = dic[cluster_num]
            else:
                l = list()

            l.append(int(user))
            dic[cluster_num] = l

        print dic

        file_name = './NewClusterResult/Cluster_Kmeans_k'+str(k)+'.csv'

        cluster_output(file_name, dic)


