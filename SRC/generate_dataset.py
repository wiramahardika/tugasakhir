import random
import sys
import csv

try:
    num_of_rows = int(sys.argv[1])
except IndexError:
    num_of_rows = 100

try:
    num_of_attr = int(sys.argv[2])
except IndexError:
    num_of_attr = 2

res = []
title_row = ["id", "label"]
for i in range(num_of_attr):
    title_row.append("attr_"+str(i))
res.append(title_row)
for i in range(num_of_rows):
    data_row = [i+1, "r-"+str(i+1)]
    rand_a = random.randint(1,200)
    rand_b = rand_a + 75
    for j in range(num_of_attr):
        data_row.append(random.randint(rand_a,rand_b))
    res.append(data_row)

csvfile = "dataset.csv"
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(res)
