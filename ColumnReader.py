__author__ = 'User'


import csv
from collections import defaultdict

columns = defaultdict(list) # each value in each column is appended to a list

with open('./DataSet/file.txt') as f:
    reader = csv.DictReader(f) # read rows into a dictionary format
    for row in reader: # read a row as {column1: value1, column2: value2,...}
        for (k,v) in row.items(): # go over each column name and value
            columns[k].append(v) # append the value into the appropriate list
                                 # based on column name k

print(columns['name'])
print(columns['phone'])
print(columns['street'])