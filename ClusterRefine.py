
__author__ = 'c11KPY'

import os.path

def refine(file):


    with open(file) as f:

        write_file_path = file.replace('.csv', '_cluster.csv')

        if os.path.exists(write_file_path):
            os.remove(write_file_path)

        users = list()
        for line in f:
            writeLine = line.strip()
            usersInCluster = list()
            values = line.split(',')
            if values[0].isalnum():

                k_value = values[0]
                valuesFloat = map(float, values)

                threshold = valuesFloat[-1]
                userValues = valuesFloat[1:-3]

                for i in xrange(len(userValues)):
                    userValue = userValues[i]
                    if userValue > threshold:
                        usersInCluster.append(users[i])

                writeLine =  str(k_value)+','+str(usersInCluster).replace('[', '').replace(']', '').replace("'", "").strip().replace('\n', '').replace('\\', '').replace('n', '')
                # print countOfNonZero
                # writeLine = str(int(k_value))+','+str(userValues).replace('[', '').replace(']', '')+','+str(countOfNonZero)+','+str(sumOfCluster)+','+str(threshold)

                with open(write_file_path, 'a') as wf:
                    wf.write(writeLine)
                    wf.write('\n')

            else:
                users = values[1:]



class cluster:

    files = ['./NewClusterResult/H_8_1e-8_refined.csv', './NewClusterResult/H_10_1e-8_refined.csv', './NewClusterResult/H_12_1e-8_refined.csv']
    for file in files:

        refine(file)

        # for value in threshold:

            # user_score_dict = load_result_from_csv(file)
            # clustering(file, user_score_dict, value)
        print file





