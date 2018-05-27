import sys
import csv
import os, shutil
import random
import json


num_of_rows = int(sys.argv[1])
try:
    num_of_cols = int(sys.argv[2])
except IndexError:
    num_of_cols = 2
data = list()
with open('covtype.data') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    init = True
    idx = 0
    haha = list()
    for row in readCSV:
        data.append(row[0:10])
        idx+=1
attribute = [
    "id",
    "label",
    "Elevation",
    "Aspect",
    "Slope",
    "Horizontal_Distance_To_Hydrology",
    "Vertical_Distance_To_Hydrology",
    "Horizontal_Distance_To_Roadways",
    "Hillshade_9am",
    "Hillshade_Noon",
    "Hillshade_3pm",
    "Horizontal_Distance_To_Fire_Points"
]

r = list(range(len(data)))
random.shuffle(r)
res = list()
res.append(attribute[0:2+num_of_cols])
idx = 0
for i in r[0:num_of_rows]:
    res_temp = [idx+1, "R"+str(idx+1)]
    res_temp += list(map(int,data[i][0:num_of_cols]))
    res.append(res_temp)
    idx+=1
with open("datasets/attribute.json", 'w') as fp:
    json.dump(attribute[0:2+num_of_cols], fp)
with open("datasets/forest_cover/dataset_"+str(num_of_rows)+"_"+str(num_of_cols)+".csv", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(res)
