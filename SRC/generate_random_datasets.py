import random
import sys
import json
import csv

try:
    num_of_rows = int(sys.argv[1])
except IndexError:
    num_of_rows = 100
try:
    num_of_cols = int(sys.argv[2])
except IndexError:
    num_of_cols = 2
with open('datasets/attribute.json') as f:
    attribute = list(json.load(f))
with open('datasets/properties.json') as f:
    properties = dict(json.load(f))
res = list()
res.append(attribute[0:2+num_of_cols])
for idx in range(0,num_of_rows):
    res_temp = [idx+1, "R"+str(idx+1)]
    for attr in attribute[2:2+num_of_cols]:
        rand_min = properties[attr]["min"]
        rand_max = properties[attr]["max"]
        res_temp.append(random.randint(rand_min,rand_max))
    res.append(res_temp)
with open("datasets/independent/dataset_"+str(num_of_rows)+"_"+str(num_of_cols)+".csv", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(res)
