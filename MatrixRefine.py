__author__ = 'c11KPY'

import os


def refine(file):


    with open(file) as f:

        write_file_path = file.replace('.csv', '_refined.csv')
        os.remove(write_file_path)

        for line in f:
            writeLine = line

            values = line.split(',')
            if values[0].isalnum():

                valuesFloat = map(float, values)
                k_value = valuesFloat[0]
                userValues = valuesFloat[1:]
                # print userValues
                sumOfCluster = sum(userValues)
                # print 'sum of cluster: '+str(sumOfCluster)
                countOfNonZero = sum(x > 0 for x in userValues)
                threshold = sumOfCluster/countOfNonZero

                # print countOfNonZero
                writeLine = str(int(k_value))+','+str(userValues).replace('[', '').replace(']', '')+','+str(countOfNonZero)+','+str(sumOfCluster)+','+str(threshold)

            with open(write_file_path, 'a') as wf:
                wf.write(writeLine.replace('\n', '')+'\n')




class cluster:
    threshold = [0.005, 0.01, 0.02, 0.03]
    files = ['./NewClusterResult/H_8_1e-8.csv', './NewClusterResult/H_10_1e-8.csv', './NewClusterResult/H_12_1e-8.csv'];
    for file in files:

        refine(file);

        # for value in threshold:

            # user_score_dict = load_result_from_csv(file)
            # clustering(file, user_score_dict, value)
        print file