__author__ = 'User'


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

class TopNMatrix:
    matrix = './DataSet/matrix.csv'
    top_n_pattern(matrix, 15)