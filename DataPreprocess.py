__author__ = 'c11KPY'
import csv
import os
import pickle


def load_csv(file_path):
     print 'load csv file...'
     user_dict = dict()   # record every user dealed information
     with open(file_path, 'rt') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            line = ', '.join(row)
            user = int(line.split(',')[1])
            if  user_dict.__contains__(user):
                lines = user_dict[user]
                lines.append(line)
            else:
                lines = list()
                lines.append(line)
                user_dict[user] = lines
     # print user_dict[6]
     return user_dict


def user_transaction_mapping(user_dict):
    user_transaction_dict = dict()
    users = sorted(user_dict.keys())
    for user in users:  # record every user transaction information in hierarchy
        lines = user_dict[user]
        time_dict = dict()

        for line in lines:
            item = int(line.split(',')[0])
            time = int(line.split(',')[2])
            if time_dict.__contains__(time):
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

        user_transaction_dict[user] = time_dict

    for user in users:
        if len(user_transaction_dict[user].keys()) == 1:
            user_transaction_dict.pop(user, None)

    filter_users = sorted(user_transaction_dict.keys())

    if not os.path.exists('./pkls'):
        os.makedirs('./pkls')

    with open("./pkls/filter_users.pkl", "wb") as wf:
        pickle.dump(filter_users, wf)



    # for user in filter_users:
    #     print user_transaction_dict[user]

    # print(user_transaction_dict[8])
    return filter_users, user_transaction_dict


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

    if not os.path.exists('./pkls'):
        os.makedirs('./pkls')

    with open("./pkls/patterns.pkl", "wb") as wf:
        pickle.dump(patterns, wf)

    return user_pattern_dic, patterns


def getAllPatterns(items1, items2, patterns):
    localPatterns = list()
    for item1 in items1:
        for item2 in items2:
            pattern = (item1, item2)
            localPatterns.append(pattern)
            # print(pattern)
            if not patterns.__contains__(pattern):
                patterns.append(pattern)
    return localPatterns

def transToMatrix(users, user_pattern_dic, patterns):

    print "transfer to matrix, please wait..."

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
            if user_pattern_dic.__contains__(user):
                if user_pattern_dic[user].__contains__(pattern):
                    count = user_pattern_dic[user][pattern]
                    user_pattern_matrix[row][column] = count
            row+=1
        column+=1

    with open("./DataSet/matrix.csv","w") as wf:
        wf.write("patterns\users,")
        for i in range(len(users)):
            wf.write(str(users[i]))
            if i != len(users)-1:
                wf.write(",")
        wf.write("\n")

        for i in range(len(user_pattern_matrix)):
            wf.write(str(patterns[i]).replace(',','-')+",")
            for j in range(len(user_pattern_matrix[i])):
                wf.write(str(user_pattern_matrix[i][j]))
                if j != len(user_pattern_matrix[i])-1:
                    wf.write(",")
            wf.write("\n")

    if not os.path.exists('./pkls'):
        os.makedirs('./pkls')
    with open("./pkls/matrix.pkl", "wb") as wf:
        pickle.dump(user_pattern_matrix, wf)

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

    with open("./DataSet/normal_matrix.csv","w") as wf:
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

    if not os.path.exists('./pkls'):
        os.makedirs('./pkls')
    with open("./pkls/normal_matrix.pkl", "wb") as wf:
        pickle.dump(user_pattern_matrix, wf)

    return user_pattern_matrix

if __name__ == '__main__':
    data_file_path = './DataSet/data.csv'
    d = load_csv(data_file_path)
    filter_users, trans_dic = user_transaction_mapping(d)
    user_pattern_dict, patterns = transToUserPatternDict(trans_dic)
    matrix = transToMatrix(filter_users, user_pattern_dict, patterns)
    normal_matrix = normalizeMatrix(filter_users, matrix, patterns)