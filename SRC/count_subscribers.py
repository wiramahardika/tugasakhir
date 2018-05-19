import json
import os, os.path
import glob
import sys
import threading
import datetime

def basic_target():
    t = dict()
    t["id"] = "target"
    t["label"] = "target"
    t["child"] = []
    t["visited"] = False
    t["is_root"] = False
    t["dominating"] = []
    t["score"] = 1
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
  i = 1;
  for record in skyline_cand:
    if is_skyline(record, skyline_cand[0:i], v, attribute):
      result.append(record)
    i+=1
  return result

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
        results.append(graph_full[x][attr])
    return tuple(results)

def search_clean_cut(graph, node, target, attribute, is_initial = False):
    if is_initial:
        child_dict = {k: v for k, v in graph.iteritems() if v["is_root"]}
    else:
        if node in visited:
            return False
        else:
            visited.append(node)
            if is_dominating(target, graph[node], attribute):
                return [str(node)]
            else:
                child_keys = graph[node]["child"]
                if len(child_keys) is 0:
                    return False
                child_dict = { key: graph[key] for key in child_keys }
    # child = sorted(child_dict, key=lambda x: (child_dict[x]['score']), reverse=True)
    child = child_dict.keys()
    cut = list()
    for next in child:
        cut_tmp = search_clean_cut(graph, next, target, attribute)
        if cut_tmp:
            cut += cut_tmp
    return cut


# ---------------------- THREADING CLASS ----------------------
class subsCount(threading.Thread):
    def __init__(self, threadID, name, graph, target, attribute):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.graph = graph
        self.target = target
        self.attribute = attribute
    def run(self):
        print "THREAD "+self.name+" started"
        gross_cut = search_clean_cut(self.graph, False, self.target, self.attribute, True)
        gross_cut = sorted(gross_cut, key=generatekey)
        clean_cut = find_skyline(gross_cut, self.graph, self.attribute)
        if len(clean_cut) > 0:
            highest_score = sorted(clean_cut, key=lambda x:(self.graph[x]["score"]), reverse=True)[0]
            potential_subs = self.graph[highest_score]["score"] + (len(clean_cut)-1)
        else:
            highest_score = "No subscriber"
            potential_subs = 0
        self.clean_cut = clean_cut
        self.highest_score = highest_score
        self.potential_subs = potential_subs


# ---------------------- MAIN PROGRAM ----------------------
time_start = datetime.datetime.now()
print "Program started"

visited = list()
with open('graph_data/graph_full.json') as f:
    data = json.load(f)
    graph_full = dict(data)
with open('graph_data/attribute.json') as f:
    data = json.load(f)
    attribute = list(data)
graph = list()
graph_file = glob.glob('graph_data/graph-*.json')
for gf in graph_file:
    with open(gf) as f:
        data = json.load(f)
    g_dict = dict(data)
    graph.append(g_dict)
target = generick_target(sys.argv[1:])
threads = []
for t in range(0,len(graph)):
    threads.append(subsCount(t+1,"Subs Counter #"+str(t+1),graph[t],target,attribute))
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
    print "Highest subscription score: "+str(t.highest_score)
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
print "\n"
results = {
    "clean_cut": clean_cut,
    "potential_subs": potential_subs
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
