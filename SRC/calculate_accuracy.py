import csv
import json


def is_dominating(subject, target, attribute):
    dominate = 0
    for attr in attribute:
        if subject[attr] > target[attr]:
            return False
        elif subject[attr] < target[attr]:
            dominate+=1
    if dominate < 1:
        return False
    else:
        return True

def basic_target():
    t = dict()
    t["id"] = "target"
    t["label"] = "target"
    return t

def generick_target(attribute):
    target = basic_target()
    attr_label = list()
    attr_value = attribute[0].split(',')
    if len(attribute) > 1:
        label = attribute[1].split(',')
        for x in label:
            attr_label.append(x)
    else:
        for x in range(len(attr_value)):
            attr_label.append("attr_"+str(x))
    for x in range(len(attr_value)):
        target[attr_label[x]] = int(attr_value[x])
    return target

def generatekey(x):
    results = list()
    for attr in attribute:
        results.append(vertex[x][attr])
    return tuple(results)

num_of_nodes = 0
vertex = dict()
attribute = list()
with open('dataset.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    init = True
    for row in readCSV:
        if init:
            attribute = list(row)
        else:
            vertex_data = dict()
            for idx in range(len(row)):
                if idx > 1:
                    vertex_data[attribute[idx]] = int(row[idx])
                else:
                    vertex_data[attribute[idx]] = row[idx]
            vertex[row[0]] = vertex_data
            num_of_nodes+=1
        init = False
with open('graph_data/countsubs_results.json') as f:
    countsubs_results = dict(json.load(f))
attribute = list(attribute[2:])
vertex_sorted = sorted(vertex, key=generatekey, reverse=True)
target = countsubs_results["target"]
potential_subs = 0
for subs in vertex_sorted:
    if is_dominating(vertex[subs], target, attribute):
        potential_subs += 1
predicted_subs = countsubs_results["potential_subs"]
difference = abs(potential_subs - predicted_subs)
error_rate = (float(difference)/float(potential_subs)) * float(100.00)
accuracy = 100.00 - error_rate
print "Actual potential subs: "+str(potential_subs)
print "Accuracy: "+str(accuracy)+"%"
