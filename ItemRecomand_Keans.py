__author__ = 'Kyo & Kao '
import csv
import matplotlib.pyplot as plt
from numpy import *

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

    wf = open("./matrix_kmeans.csv","w")
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
    wf.close()
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

    wf = open("./normal_matrix_kmeans.csv","w")
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
    wf.close()
    return user_pattern_matrix

# def loadDataSet(fileName):      #general function to parse tab -delimited floats
#     dataMat = []                #assume last column is target value
#     fr = open(fileName)
#     for line in fr.readlines():
#         curLine = line.strip().split('\t')
#         fltLine = map(float,curLine) #map all elements to float()
#         dataMat.append(fltLine)
#     return dataMat

def distEclud(vecA, vecB):
    return sqrt(sum(power(vecA - vecB, 2))) #la.norm(vecA-vecB)

def randCent(dataSet, k):
    n = shape(dataSet)[1]
    centroids = mat(zeros((k,n)))#create centroid mat
    for j in range(n):#create random cluster centers, within bounds of each dimension
        minJ = min(dataSet[:,j])
        rangeJ = float(max(dataSet[:,j]) - minJ)
        centroids[:,j] = mat(minJ + rangeJ * random.rand(k,1))
    return centroids

def kMeans(dataSet, k, distMeas=distEclud, createCent=randCent):
    m = shape(dataSet)[0]  # instance count
    #record every instance which belong to cluster and cluster centroid distance.
    clusterAssment = mat(zeros((m,2)))#create mat to assign data points
                                      #to a centroid, also holds SE of each point
    centroids = createCent(dataSet, k)
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        for i in range(m):#for each data point assign it to the closest centroid
            minDist = inf; minIndex = -1
            for j in range(k):
                distJI = distMeas(centroids[j,:],dataSet[i,:])
                if distJI < minDist:
                    minDist = distJI; minIndex = j
            if clusterAssment[i,0] != minIndex: clusterChanged = True
            clusterAssment[i,:] = minIndex,minDist**2
        print centroids
        for cent in range(k):#recalculate centroids
            ptsInClust = dataSet[nonzero(clusterAssment[:,0].A==cent)[0]]#get all the point in this cluster
            centroids[cent,:] = mean(ptsInClust, axis=0) #assign centroid to mean
    return centroids, clusterAssment

class Module_data_mining:
    path = "./data.csv"
    d = load_csv(path)
    users = d.keys()
    trans_dic = user_transaction_mapping(d)

    user_pattern_dict, patterns = transToUserPatternDict(trans_dic)
    matrix = transToMatrix(users, user_pattern_dict, patterns)
    # normal_matrix = normalizeMatrix(users, matrix, patterns)

    # 1) Execute the k-means cluster algorithm
    k = 4 # How many clusters?
    rst = kMeans(matrix,k)

    # 2) Output the centroid
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x=array(rst[0][:,0]).flatten(), y=array(rst[0][:,1]).flatten(), c='pink', s=80)

    # 3) Output the dataset with different according to its cluster.
    color = ['red', 'blue', 'green', 'yellow']
    for i in range(k):
        smc = matrix[nonzero(rst[1][:,0].A==i)[0]] # sub data set of each cluster.
        ax.scatter(x=array(smc[:,0]).flatten(), y=array(smc[:,1]).flatten(), c=color[i], s=30)
    plt.show()


