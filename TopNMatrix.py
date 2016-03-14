__author__ = 'User'

import csv
from operator import itemgetter

def top_n_pattern(matrix_path, n):

    matrix_top_n = matrix_path.replace('.csv', '_top_'+str(n)+'.csv')

    row = 0;

    lineDic = dict()

    tuple_list = list()

    with open(matrix_path) as rf:

        for line in rf:
            line = line.strip()

            line_split = line.split(',')

            lineDic[line_split[0]] = line

            # print line_split[0]

            count = 0
            for i in xrange(len(line_split)):

                if i != 0:
                    value = line_split[i]
                    count += int(value)

            tuple_list.append((line_split[0], count))

            # print line_split[0]+'\t'+str(count)
            row += 1



    tuple_list = sorted(tuple_list, reverse=True, key=itemgetter(1))



    # print lineDic

    with open(matrix_top_n, 'w') as wf:
        for i in xrange(n+1):
            tup = tuple_list[i]
            # print tup
            print lineDic[tup[0]]
            wf.write(lineDic[tup[0]]+'\n')

def gen_normal_top_n_matrix(matrix_top_n, n):
    f = csv.reader(open(matrix_top_n))
    users = list(f.next())
    users.pop(0)

    columns = zip(*f)
    patterns = columns.pop(0)

    # print users
    # print patterns

    user_pattern_matrix = [[0 for x in range(len(users))] for y in range(len(patterns))]

    with open(matrix_top_n) as rf:

        row = 0

        for line in rf:

            if row == 0:
                row += 1
                continue

            values = line.strip().split(',')

            for j in xrange(len(values)):

                if j == 0:
                    continue

                user_pattern_matrix[row-1][j-1] = int(values[j])
                # print values[j]



            row += 1


    # print user_pattern_matrix


    # for i in range(len(user_pattern_matrix)):
    #     line = ''
    #     for j in range(len(user_pattern_matrix[i])):
    #         line += str(user_pattern_matrix[i][j])
    #         if j != len(user_pattern_matrix[i])-1:
    #             line += ','
    #     print line


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


    # for i in range(len(user_pattern_matrix)):
    #     line = ''
    #     for j in range(len(user_pattern_matrix[i])):
    #         line += str(user_pattern_matrix[i][j])
    #         if j != len(user_pattern_matrix[i])-1:
    #             line += ','
    #     print line

    with open("./DataSet/normal_matrix_top_"+str(n)+"_.csv", "w") as wf:
        wf.write("patterns\users,")
        for i in range(len(users)):
            wf.write(str(users[i]))
            if(i != len(users)-1):
                wf.write(",")
        wf.write("\n")

        for i in range(len(user_pattern_matrix)):
            wf.write(str(patterns[i])+",")
            for j in range(len(user_pattern_matrix[i])):
                wf.write(str(user_pattern_matrix[i][j]))
                if(j != len(user_pattern_matrix[i])-1):
                    wf.write(",")
            wf.write("\n")

class TopNMatrix:

    n = 15

    matrix = './DataSet/matrix.csv'
    # top_n_pattern(matrix, n)
    matrix_top_n = matrix.replace('.csv', '_top_'+str(n)+'.csv')

    gen_normal_top_n_matrix(matrix_top_n, n)