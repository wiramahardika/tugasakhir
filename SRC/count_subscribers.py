import json
import glob
import sys
import threading
import datetime

def basic_target():
    t = dict()
    t["id"] = "target"
    t["label"] = "target"
    t["child"] = 0
    t["parent"] = 0
    t["visited"] = False
    t["is_root"] = False
    return t

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

def find_bottom(set, v, attribute):
    bottom_cand = list(set)
    result = []
    i = 1;
    for cand in bottom_cand:
        is_bottom = True
        for r in bottom_cand:
            if r is cand:
                continue
            else:
                if is_dominating(v[cand], v[r], attribute):
                    is_bottom = False
                    break
        if is_bottom:
            result.append(cand)
    return result

def generick_target(attr_input, attribute):
    target = basic_target()
    attr_value = attr_input[0].split(',')
    for x in range(len(attribute)):
        target[attribute[x]] = int(attr_value[x])
    return target

def calculate_cost(preference, g, attribute):
    cost = 0
    is_first = True
    for attr in attribute:
        cost += preference[attr]
        is_first = False
    return cost

def generatekey(x):
    results = list()
    for attr in attribute:
        results.append(graph_full[x][attr])
    return tuple(results)

def search_clean_cut(graph, node, target, edges, attribute, is_initial = False):
    cut = list()
    clean_cut = list()
    if is_initial:
        child_dict = {k: v for k, v in graph.iteritems() if v["is_root"]}
        child = child_dict.keys()
    else:
        if node in visited:
            return (None,None)
        else:
            child = [d['to'] for d in edges if d['from'] == node]
    debug_cut = list()
    if is_initial or is_dominating(graph[node], target, attribute):
        is_clean_cut = False
        for next in child:
            cut_tmp,clean_cut_tmp = search_clean_cut(graph, next, target, edges, attribute)
            if not(cut_tmp is None):
                cut += cut_tmp
                clean_cut += clean_cut_tmp
                if len(cut_tmp) is 0:
                    is_clean_cut = True
                    debug_cut.append(next)
                else:
                    visited.append(next)
        if node:
            cut.append(node)
            if is_clean_cut:
                if node == '7':
                    print 'haha',debug_cut
                clean_cut.append(node)
    return (cut, clean_cut)


# ---------------------- THREADING CLASS ----------------------
class subsCount(threading.Thread):
    def __init__(self, threadID, name, graph, target, edges, attribute):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.graph = graph
        self.target = target
        self.edges = edges
        self.attribute = attribute
    def run(self):
        print "THREAD "+self.name+" started"
        gross_cut,clean_cut = search_clean_cut(self.graph, False, self.target, self.edges, self.attribute, True)
        potential_subs = len(gross_cut)
        self.clean_cut = clean_cut
        self.potential_subs = potential_subs


# ---------------------- MAIN PROGRAM ----------------------
time_start = datetime.datetime.now()
print "Program started"

visited = list()
with open('graph_data/graph_full.json') as f:
    data = json.load(f)
    graph_full = dict(data)
with open('datasets/attribute.json') as f:
    data = json.load(f)
    attribute = list(data)
with open('graph_data/edges_full.json') as f:
    data = json.load(f)
    edges = list(data)
graph = list()
graph_file = glob.glob('graph_data/graph-*.json')
graph_file.sort()
for gf in graph_file:
    with open(gf) as f:
        data = json.load(f)
    g_dict = dict(data)
    graph.append(g_dict)
target = generick_target(sys.argv[1:], attribute)
threads = []
for t in range(0,len(graph)):
    threads.append(subsCount(t+1,"Subs Counter #"+str(t+1),graph[t],target,edges,attribute))
for t in threads:
    t.start()
for t in threads:
    t.join()
print "\n\n====================\n"
clean_cut = list()
potential_subs = 0
graph_results = list()
for t in threads:
    print t.name+" RESULTS:"
    print "Clean cut: "+",".join(str(x) for x in t.clean_cut)
    print "Potential subscribers: "+str(t.potential_subs)
    clean_cut += t.clean_cut
    potential_subs += t.potential_subs
    graph_results_data = {
        "clean_cut": t.clean_cut,
        "potential_subs": t.potential_subs
    }
    graph_results.append(graph_results_data)
print "\n\n====================\n"
print "FINAL RESULTS:"
print "Clean cut: "+",".join(str(x) for x in clean_cut)
print "Potential subscribers: "+str(potential_subs)
cost = calculate_cost(target, graph_full, attribute)
print "Cost: " + str(cost)
print "\n"
results = {
    "clean_cut": clean_cut,
    "potential_subs": potential_subs,
    "cost": cost
}

results_json = {
    "target": target,
    "graph_results": graph_results,
    "results": results
}
with open("graph_data/countsubs_results.json", 'w') as fp:
  json.dump(results_json, fp)

print "RUNTIME RESULTS:"
time_end = datetime.datetime.now()
full_runtime = time_end - time_start
print "Program finished with runtime " + str(full_runtime)
print "\n"
