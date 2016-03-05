

def pruning(matrix_path):

    matrix_path_simple = matrix_path.replace('.csv', '_simple.csv')
    with open(matrix_path_simple, 'w') as wf:
        with open(matrix_path) as rf:
            for line in rf:
                line = line.strip()
                line_split = line.split(',')

                new_line = ''
                for i in xrange(len(line_split)):

                    new_line += line_split[i]
                    if i != 29:
                        new_line += ','

                    if i == 29:
                        break

                print new_line
                wf.write(new_line+'\n')

class DataPrune:
    matrix = './DataSet/matrix.csv'
    pruning(matrix)