import csv
import glob
from collections import defaultdict
import os
import operator
from operator import itemgetter

def load_matrix(matrix_path):

    user_pattern_dict = dict()

    pattern_num_dict = dict()
    lines = list()

    line_num = 0

    with open(matrix_path) as rf:

        for line in rf:
            line = line.strip()

            if line_num == 0:
                line_num += 1
                continue

            line_split = line.split(',')
            count = 0
            for column_num in xrange(len(line_split)-1):
                count += int(line_split[column_num+1])

            pattern_num_dict[line_split[0]] = count
            # print line_split[0]+'\t'+str(count)
            line_num += 1

    f = csv.reader(open(matrix_path))
    users = list(f.next())
    users.pop(0)

    columns = zip(*f)
    patterns = columns.pop(0)

    with open('./DataSet/top_15_user_pattern.csv', 'w') as wf:

        wf.write('User ID'+','+'Patterns\n')

        for i in xrange(len(users)):
            user = users[i].strip()

            row = 0
            own_patterns = list()
            for pattern_value in columns[i]:
                if int(pattern_value) > 0:
                    own_patterns.append(patterns[row])
                    # print patterns[row]
                row += 1
            wf.write(user+',')
            for j in xrange(len(own_patterns)):
                wf.write(own_patterns[j])
                if j != len(own_patterns)-1:
                    wf.write(',')
            wf.write('\n')
            user_pattern_dict[user] = own_patterns

    # print user_pattern_dict
    return pattern_num_dict, user_pattern_dict


def gen_cluster_top15_patterns(pattern_num_dict, user_pattern_dict):
    # print pattern_num_dict

    for cluster_file in glob.glob("./NewClusterResult/H_*_refined_cluster.csv"):
        # print cluster_file

        with open(cluster_file.replace('.csv', '_patterns_top_15_.csv'), 'w') as wf:

            with open(cluster_file) as rf:
                for line in rf:

                    users = line.split(',')
                    k_num = users.pop(0)
                    # print k_num

                    patterns_of_cluster = list()

                    for user in users:
                        user = user.strip()
                        if user_pattern_dict.__contains__(user):
                            patterns_of_user = user_pattern_dict[user]

                            for pattern in patterns_of_user:
                                if not patterns_of_cluster.__contains__(pattern):
                                    patterns_of_cluster.append(pattern)

                            # print patterns_of_user

                    tuple_list = list()
                    # print len(patterns_of_cluster)
                    patterns_of_cluster = set(patterns_of_cluster)

                    # print pattern_num_dict

                    for pattern in patterns_of_cluster:
                        num = pattern_num_dict[pattern]
                        tuple_list.append((pattern, num))
                        # print num
                    tuple_list = sorted(tuple_list, reverse=True, key=itemgetter(1))

                    tuple_list = tuple_list[:10]

                    tuple_line = ''

                    for i in xrange(len(tuple_list)):
                        pattern_tuple = tuple_list[i]

                        first_value = pattern_tuple[0]
                        second_value = pattern_tuple[1]
                        tuple_line += first_value+':'+str(second_value)

                        if i != len(tuple_list)-1:
                            tuple_line += ','

                    wf.write(str(k_num)+','+str(tuple_line)+'\n')


class info_statistics:
    matrix_path = './DataSet/matrix_top_15.csv'
    pattern_num_dict, user_pattern_dict = load_matrix(matrix_path)
    gen_cluster_top15_patterns(pattern_num_dict, user_pattern_dict)



    # out_user_patterns(matrix)


