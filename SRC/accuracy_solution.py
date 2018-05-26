import csv
import json
import copy
import itertools
from operator import itemgetter
import sys


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
# with open('graph_data/solution_result.json') as f:
#     solution_result = dict(json.load(f))
with open('graph_data/countsubs_results.json') as f:
    countsubs_results = dict(json.load(f))
target = countsubs_results["target"]
attribute = list(attribute[2:])
attr_value_cand = list()
solution_cand = list()
for attr in attribute:
    attr_value_cand.append(range(1,(target[attr]+1)))
    print attr_value_cand
# print attr_value_cand
sys.exit(0)
for combination in list(itertools.product(*attr_value_cand)):
    attr_comb = list(combination)
    for a in range(len(attribute)):
        target[attribute[a]] = combination[a]
    potential_subs = 0
    for subs in vertex:
        if is_dominating(target, vertex[subs], attribute):
            potential_subs += 1
    if potential_subs >= solution_result["expected_subs"]:
        cost = 0
        for attr_val in combination:
            cost += attr_val
        attr_comb.append(potential_subs)
        attr_comb.append(cost)
        solution_cand.append(attr_comb)
best_candidate = sorted(solution_cand, key=itemgetter(-1), reverse=True)[0]
cost = best_candidate[-1]
cost_diff = countsubs_results["results"]["cost"] - cost
difference = abs(solution_result["cost_diff"] - cost_diff)
error_rate = (float(difference)/float(cost_diff)) * float(100.00)
accuracy = 100.00 - error_rate
if accuracy < 0.0:
    accuracy = 0.0
print "\n\n====================\n"
print "SOLUTION RESULTS:"
print "New Preference: ",solution_result["preference"]
print "Cost difference: " + str(solution_result["cost_diff"])
print "Potential subscribers: "+str(solution_result["potential_subs"])
print "\n\n====================\n"
print "BEST ACTUAL RESULTS:"
print "New Preference: ",best_candidate[:-2]
print "Cost difference: " + str(cost_diff)
print "Potential subscribers: "+str(best_candidate[-2])
print "\n\n====================\n"
print "SUMMARY:"
print "Accuracy: " + str(accuracy) + "%"
print "\n\n====================\n"
