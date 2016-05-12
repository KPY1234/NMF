from operator import itemgetter
import math
import os



def loadData(file):

    user_tup_dic = dict()

    with open(file) as f:

        row = 0
        users = list()

        for line in f:

            if row == 0:
                users = line.strip().split(",")[1:]
                # print users
            else:
                user_value_tup_list = list()
                values = line.strip().split(",")[1:]
                values = map(float, values)
                for i in xrange(len(values)):
                    value = values[i]
                    if value != 0:
                        user_value_tup_list.append((users[i], values[i]))
                user_tup_dic[row] = user_value_tup_list
                # print user_value_tup_list
            row += 1

    return user_tup_dic


def coe_cluster(file, user_tup_dic, threshold):

    file_path = os.path.abspath(file)
    file_path = file_path.replace(".csv", "_coef_thres_"+str(threshold)+".csv")

    with open(file_path, 'w') as wf:

        # print file_path

        key_num = len(user_tup_dic.keys())

        for i in xrange(key_num):

            wf.write(str(i)+',')

            user_value_tup_list = user_tup_dic.get(i+1)
            list_size = len(user_value_tup_list)
            median = int(math.ceil(list_size/2))
            user_value_tup_list.sort(key=itemgetter(1), reverse=True)

            begin = median - int(list_size*(threshold/100.0))
            if begin < 0:
                begin = 0
            end = median + int(list_size*(threshold/100.0))
            if end > list_size:
                end = list_size

            part_user_value_tup_list = user_value_tup_list[begin:end]

            for tup in part_user_value_tup_list:
                wf.write(str(tup[0])+',')
            wf.write('\n')

            # for tup in part_user_value_tup_list:
            #     wf.write(str(tup[1]) + ',')
            # wf.write('\n')

            print str(i)+'\t'+str(part_user_value_tup_list)

            # print str(len(user_value_tup_list))+'\t'+str(median)+'\t'+str(user_value_tup_list[median])
            # print str(i)+'\t'+str(user_value_tup_list)



class cluster:

    threshold = 10

    files = ['./NewClusterResult/H_8_1e-8.csv']
    # files = ['./NewClusterResult/H_8_1e-8.csv', './NewClusterResult/H_10_1e-8.csv', './NewClusterResult/H_12_1e-8.csv']
    for file in files:
        user_tup_dic = loadData(file)

        coe_cluster(file, user_tup_dic, threshold)

        # for value in threshold:

            # user_score_dict = load_result_from_csv(file)
            # clustering(file, user_score_dict, value)
        print file