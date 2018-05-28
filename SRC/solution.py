import json
import glob
import sys
import datetime
import time
import os, shutil
import psutil
import resource
import csv


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

def is_skyline(target, set, v, attribute):
    skyline_cand = list(set)
    for candidate in skyline_cand:
        if target is candidate:
            continue
        elif is_dominating(v[candidate], v[target], attribute):
            return False
    return True

def find_skyline(set, v, attribute):
    skyline_cand = list(set)
    result = []
    i = 1
    for record in skyline_cand:
        if is_skyline(record, skyline_cand[0:i], v, attribute):
            result.append(record)
        i+=1
    return result

def normalize_attr(min, max, x):
    return (float(1-min)+float(x))/(float(1-min)+float(max))

def find_new_clean_cut(graph, node, min_subs, edges, attribute, root = [], is_initial = False):
    cut = list()
    clean_cut = list()

    if is_initial:
        child = root
    else:
        if node in node_visited:
            return list()
        else:
            node_visited.append(node)
            if graph[node]["score"] >= min_subs:
                return [node]
            child = [d['to'] for d in edges if d['from'] == node]
    for next in child:
        cut += find_new_clean_cut(graph, next, min_subs, edges, attribute)
    return cut

ts = time.time()
st_start = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d__%H:%M:%S')
time_start = datetime.datetime.now()
print "Program started"
expected_subs = int(sys.argv[1])
try:
    session = sys.argv[3].split(',')
    session_name = session[0]
    session_type = session[1]
    session_full_id = "_"+session_name+"_"+session_type
except IndexError:
    session = False
    session_name = ""
    session_type = ""
    session_full_id = ""
with open('session'+session_full_id+'/countsubs_results.json') as f:
    countsubs_results = dict(json.load(f))
with open('session'+session_full_id+'/edges.json') as f:
    edges = list(json.load(f))
with open('session'+session_full_id+'/attribute.json') as f:
    attribute = list(json.load(f))
with open('session'+session_full_id+'/graph.json') as f:
    graph = dict(json.load(f))
with open('session'+session_full_id+'/clean_cut_layer.json') as f:
    clean_cut_layer = dict(json.load(f))
with open('session'+session_full_id+'/properties.json') as f:
    properties = dict(json.load(f))
try:
    weight_inp = sys.argv[2]
    weight_list = weight_inp.split(',')
    weight = dict()
    for i in range(len(attribute)):
        weight[attribute[i]] = float(weight_list[i])
except IndexError:
    weight = dict()
    weight_default = 1.0/float(len(attribute))
    for i in range(len(attribute)):
        weight[attribute[i]] = weight_default
print weight
layer_indices = clean_cut_layer.keys()
layer_indices = sorted(map(int, layer_indices))
layer = str([l for l in layer_indices if l <= expected_subs][-1])
node_visited = list()
new_clean_cut = find_new_clean_cut(graph, False, expected_subs, edges, attribute, clean_cut_layer[layer], True)
# new_clean_cut = find_skyline(new_clean_cut, graph, attribute)
solution = None
solution_cost = 999.0
normalized_before = dict()
for attr in attribute:
    normalized_before[attr] = normalize_attr(properties[attr]["min"], properties[attr]["max"], countsubs_results["target"][attr])
print normalized_before
for new in new_clean_cut:
    print new
    cost_attr = dict()
    cost = 0.0
    for attr in attribute:
        normalized_after = normalize_attr(properties[attr]["min"], properties[attr]["max"], graph[new][attr])
        cost += ((normalized_after - normalized_before[attr]) * (1.0 - weight[attr]))
        print attr,":",graph[new][attr],((normalized_after - normalized_before[attr]) * weight[attr])
    if cost < solution_cost:
        solution = new
        solution_cost = cost
    print "subscribers :",graph[new]["score"]
    print "cost :",cost
    print "\n"
print "BEST SOLUTION:"
print solution
for attr in attribute:
    print attr,":",graph[solution][attr]
print "subscribers :",graph[solution]["score"]
print "cost :",solution_cost
print "\n"

print "\nRUNTIME RESULTS:"
print "Number of nodes: "+str(len(graph))
time_end = datetime.datetime.now()
full_runtime = time_end - time_start
print "Program finished with runtime " + str(full_runtime)
process = psutil.Process(os.getpid())
mem_usage = float(process.memory_info().rss)/1000000.0
print "Memory usage:",mem_usage

res = list()
ts = time.time()
st_end = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d__%H:%M:%S')
res_data = list()
res_data.append(st_start)
res_data.append(st_end)
res_data.append("algo1")
res_data.append(len(graph))
res_data.append(len(attribute))
res_data.append(session_type)
res_data.append(expected_subs)
initial_value = list()
recomended_value = list()
weight_list = list()
for attr in attribute:
    initial_value.append(countsubs_results["target"][attr])
    recomended_value.append(graph[solution][attr])
    weight_list.append(weight[attr])
res_data.append("|".join(list(map(str, weight_list))))
res_data.append("|".join(list(map(str, initial_value))))
res_data.append("|".join(list(map(str, recomended_value))))
res_data.append(graph[solution]["label"])
res_data.append(solution_cost)
res_data.append(full_runtime)
res_data.append(mem_usage)
res.append(res_data)
if session:
    with open("session_log/solution_script.csv", "a") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(res)
else:
    with open("session_log/solution_manual.csv", "a") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(res)
