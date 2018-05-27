import random
import datetime
import threading
import json
import sys
import csv
import copy

def format_graph(v, node):
    v_local = dict(v)
    result = dict()
    for x in node:
        result[x] = copy.deepcopy(v_local[x])
        parent = len(result[x]["parent"])
        result[x].pop("parent", None)
        result[x]["parent"] = parent
        child = len(result[x]["child"])
        result[x].pop("child", None)
        result[x]["child"] = child
    return result

def format_nodes(v, node):
    v_local = copy.deepcopy(v)
    result = list()
    for x in range(len(node)):
        v_local[node[x]]["label"] += "\n("
        a_idx = 0
        for a in attribute_value:
            if a_idx == 0:
                v_local[node[x]]["label"] += str(v_local[node[x]][a])
            else:
                v_local[node[x]]["label"] += ","+str(v_local[node[x]][a])
            a_idx+=1
        # v_local[node[x]]["label"] += ")"
        v_local[node[x]]["label"] += ")\n"+str(len(v_local[node[x]]['parent']))
        result.append(v_local[node[x]])
    return result

def format_edges(v, node):
    v_local = dict(v)
    result = list()
    for x in node:
        for child in v_local[x]["child"]:
            result_data = {
                "from": x,
                "to": child
            }
            result.append(result_data)
    return result

def format_layer(v, node, start_point, edges, attribute, cut_size = False):
    global node_visited
    v_local = dict(v)
    result = dict()
    num_of_nodes = len(node)
    if not cut_size:
        cut_size = num_of_nodes/2
    for layer in range(0,num_of_nodes+1,cut_size):
        result_temp = search_clean_cut(v_local, False, layer, edges, attribute, start_point, True)
        result_temp = sorted(result_temp, key=generatekey)
        result_temp = find_skyline(result_temp, v_local)
        result[layer] = result_temp
        start_point = result[layer]
        node_visited = list()
    return result

def search_clean_cut(graph, node, layer_size, edges, attribute, root = [], is_initial = False):
    cut = list()
    clean_cut = list()
    if is_initial:
        child = root
    else:
        if node in node_visited:
            return list()
        else:
            node_visited.append(node)
            if graph[node]["parent"] >= layer_size:
                return [node]
            child = [d['to'] for d in edges if d['from'] == node]
    for next in child:
        cut += search_clean_cut(graph, next, layer_size, edges, attribute)
    return cut

def slice_vertex(v, max):
  v_thread = []
  for x in range(0,len(v),max):
    v_thread.append(v[x:x+max])
  return v_thread

def remove_from_list(origin, to_remove, exception = []):
  temp = set(to_remove)
  result = [value for value in origin if value not in to_remove or value in exception]
  return result

def merge(first_list, second_list):
  return first_list + list(set(second_list) - set(first_list))

def is_dominating(subject, target):
    dominate = 0
    for attr in attribute_value:
        if subject[attr] > target[attr]:
            return False
        elif subject[attr] < target[attr]:
            dominate+=1
    if dominate < 1:
        return False
    else:
        return True

def is_skyline(target, set, v):
  skyline_cand = list(set)
  for candidate in skyline_cand:
    if target is candidate:
      continue
    elif is_dominating(v[candidate], v[target]):
      return False
  return True

def find_skyline(set, v):
  skyline_cand = list(set)
  result = []
  i = 1;
  for record in skyline_cand:
    if is_skyline(record, skyline_cand[0:i], v):
      result.append(record)
    i+=1
  return result

def find_dominating(r, set, v):
    return [s for s in set if is_dominating(v[r],v[s])]

def progress_report(node):
  global node_visited
  global num_of_nodes
  node_visited = merge(node_visited, [node])
  progress = float(len(node_visited))/float(num_of_nodes)*float(100)
  sys.stdout.write("\rNumber of visited nodes: " + str(len(node_visited)) + " of " + str(num_of_nodes) + " nodes --- " + str(progress) + "%")
  sys.stdout.flush()

class theThread(threading.Thread):
    def __init__(self, idx, v_node):
        threading.Thread.__init__(self)
        self.idx = idx
        self.v_node = v_node
    def run(self):
        v_temp = self.v_node[self.idx:]
        for s in range(len(v_temp)):
            # print self.v_node[self.idx],v_temp[s],self.v_node[self.idx:]
            if is_dominating(vertex[self.v_node[self.idx]],vertex[v_temp[s]]):
                if is_skyline(v_temp[s], vertex[self.v_node[self.idx]]["dominating"], vertex):
                    vertex[self.v_node[self.idx]]["child"].append(v_temp[s])
                vertex[self.v_node[self.idx]]["dominating"].append(v_temp[s])
                vertex[v_temp[s]]["ancestor"].append(self.v_node[self.idx])

def find_dominating_prop(v_node):
    threads = []
    for t in range(0,len(v_node)):
      threads.append(theThread(t, v_node))

    for t in threads:
      t.start()

    for t in threads:
      t.join()


def generatekey(x):
    results = list()
    for attr in attribute_value:
        results.append(vertex[x][attr])
    return tuple(results)

def build_graph(node, thread_vertex, sub_vertex, is_initial = False):
    if not is_initial:
        if vertex[node]["visited"] or node not in thread_vertex:
            return
        else:
            child_cand = list(find_dominating(node, sub_vertex, vertex))
            vertex[node]["visited"] = True
            for c in child_cand:
                if node not in vertex[c]["parent"]:
                    vertex[c]["parent"].append(node)
    else:
        child_cand = thread_vertex
    child = find_skyline(child_cand, vertex)
    sub_vertex_cand = remove_from_list(list(child_cand), child)
    if not is_initial:
        vertex[node]["child"] = child
        # progress_report(node)
    for record in child:
        if is_initial:
            index_cut = sub_vertex.index(record)
            build_graph(record, thread_vertex, sub_vertex[index_cut:])
        else:
            build_graph(record, thread_vertex, sub_vertex_cand)
    return

class cdgThread(threading.Thread):
  def __init__(self, threadID, name, thread_vertex, sub_vertex):
    threading.Thread.__init__(self)
    self.threadID = threadID
    self.name = name
    self.thread_vertex = thread_vertex
    self.sub_vertex = sub_vertex
  def run(self):
    print "\nTHREAD "+self.name+" started"
    build_graph(None, self.thread_vertex, self.sub_vertex, True)
    t_end = datetime.datetime.now()
    self.runtime = t_end - time_start
    print "THREAD "+self.name+" finished with runtime " + str(self.runtime)

time_start = datetime.datetime.now()
print "Program started"
count = 0
node_visited = []
num_of_nodes = 0
try:
    max_nodes_in_thread = int(sys.argv[1])
except IndexError:
    max_nodes_in_thread = 10000

try:
    cut_size = int(sys.argv[2])
except IndexError:
    cut_size = False

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
            vertex[row[0]]["child"] = []
            vertex[row[0]]["parent"] = []
            vertex[row[0]]["dominating"] = []
            vertex[row[0]]["ancestor"] = []
            vertex[row[0]]["visited"] = False
            vertex[row[0]]["is_root"] = False
            num_of_nodes+=1
        init = False

attribute_value = list(attribute[2:])
vertex_sorted = sorted(vertex, key=generatekey)
vertex_thread = slice_vertex(vertex_sorted, max_nodes_in_thread)

find_dominating_prop(vertex_sorted)
# print vertex
# sys.exit(0)
# threads = []
# for t in range(0,len(vertex_thread)):
#   threads.append(cdgThread(t+1,"Graph Builder #"+str(t+1),vertex_thread[t],vertex_sorted))
#
# for t in threads:
#   t.start()
#
# for t in threads:
#   t.join()

import os, shutil
folder = 'graph_data'
for the_file in os.listdir(folder):
    file_path = os.path.join(folder, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)

graph = format_graph(vertex, vertex_sorted)
nodes = format_nodes(vertex, vertex_sorted)
edges = format_edges(vertex, vertex_sorted)
node_visited = list()
first_layer_root = {k: v for k, v in vertex.iteritems() if v["is_root"]}
first_layer_root = first_layer_root.keys()
clean_cut_layer = format_layer(graph, vertex_sorted, first_layer_root, edges, attribute_value, cut_size)
with open("graph_data/graph_full.json", 'w') as fp:
  json.dump(graph, fp)
with open("graph_data/nodes_full.json", 'w') as fp:
  json.dump(nodes, fp)
with open("graph_data/edges_full.json", 'w') as fp:
  json.dump(edges, fp)
with open("graph_data/attribute.json", 'w') as fp:
  json.dump(attribute_value, fp)
with open("graph_data/clean_cut_layer.json", 'w') as fp:
  json.dump(clean_cut_layer, fp)
print "\nRUNTIME RESULTS:"
print "Number of nodes: "+str(num_of_nodes)
# for t in threads:
#   print "THREAD "+t.name+" finished with runtime " + str(t.runtime)

time_end = datetime.datetime.now()
full_runtime = time_end - time_start
print "Program finished with runtime " + str(full_runtime)
