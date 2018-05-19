import random
import datetime
import threading
import json
import sys
import csv
import copy

def format_graph(v, node):
  v_local = copy.deepcopy(v)
  result = dict()
  for x in node:
    result[x] = v_local[x]
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
        v_local[node[x]]["label"] += ")\n"+str(v_local[node[x]]['score'])
        result.append(v_local[node[x]])
    return result

def format_edges(v, node):
    v_local = copy.deepcopy(v)
    result = list()
    for x in node:
        for child in v_local[x]["child"]:
            result_data = {
                "from": x,
                "to": child
            }
            result.append(result_data)
    return result

def slice_vertex(v, max):
  v_thread = []
  for x in range(0,len(v),max):
    v_thread.append(v[x:x+max])
  return v_thread

def remove_from_list(origin, to_remove):
  temp = set(to_remove)
  result = [value for value in origin if value not in to_remove]
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
  result = []
  for s in set:
    if r is s:
      continue
    elif is_dominating(v[r], v[s]):
      result.append(s)
  return result

def progress_report(node):
  global node_visited
  global num_of_nodes
  node_visited = merge(node_visited, [node])
  progress = float(len(node_visited))/float(num_of_nodes)*float(100)
  sys.stdout.write("\rNumber of visited nodes: " + str(len(node_visited)) + " of " + str(num_of_nodes) + " nodes --- " + str(progress) + "%")
  sys.stdout.flush()

def generatekey(x):
    results = list()
    for attr in attribute_value:
        results.append(vertex[x][attr])
    return tuple(results)

def build_graph(node, layer, is_initial = False):
  if not is_initial:
    if vertex[node]["visited"]:
      return
    else:
      vertex[node]["visited"] = True
      layer = list(find_dominating(node, layer, vertex))
      vertex[node]["score"] += len(layer)
      for attr in attribute_value:
        vertex[node]["worth_point"] += float(vertex[node][attr])
      vertex[node]["worth_point"] = float(vertex[node]["worth_point"])/float(vertex[node]["score"])
      # vertex[node]["dominating"] = merge(vertex[node]["dominating"], layer)

  child = find_skyline(layer, vertex)
  layer_cand = remove_from_list(list(layer), child)

  if not is_initial:
    vertex[node]["child"] = child
    progress_report(node)

  for record in child:
    if is_initial:
      vertex[record]["is_root"] = True
    build_graph(record, layer_cand)

  return

class cdgThread(threading.Thread):
  def __init__(self, threadID, name, layer):
    threading.Thread.__init__(self)
    self.threadID = threadID
    self.name = name
    self.layer = layer
  def run(self):
    print "\nTHREAD "+self.name+" started"
    build_graph(None, self.layer, True)
    self.graph = format_graph(vertex, self.layer)
    self.nodes = format_nodes(vertex, self.layer)
    self.edges = format_edges(vertex, self.layer)
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
            vertex[row[0]]["visited"] = False
            vertex[row[0]]["is_root"] = False
            vertex[row[0]]["dominating"] = []
            vertex[row[0]]["score"] = 1
            vertex[row[0]]["worth_point"] = 0
            num_of_nodes+=1
        init = False

attribute_value = list(attribute[2:])
vertex_sorted = sorted(vertex, key=generatekey)
vertex_thread = slice_vertex(vertex_sorted, max_nodes_in_thread)

threads = []
for t in range(0,len(vertex_thread)):
  threads.append(cdgThread(t+1,"Graph Builder #"+str(t+1),vertex_thread[t]))

for t in threads:
  t.start()

for t in threads:
  t.join()

import os, shutil
folder = 'graph_data'
for the_file in os.listdir(folder):
    file_path = os.path.join(folder, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)

tree_idx = 1
for t in threads:
  with open("graph_data/graph-"+str(tree_idx)+".json", 'w') as fp:
    json.dump(t.graph, fp)
  with open("graph_data/nodes-"+str(tree_idx)+".json", 'w') as fp:
    json.dump(t.nodes, fp)
  with open("graph_data/edges-"+str(tree_idx)+".json", 'w') as fp:
    json.dump(t.edges, fp)
  tree_idx+=1

graph = format_graph(vertex, vertex_sorted)
nodes = format_nodes(vertex, vertex_sorted)
edges = format_edges(vertex, vertex_sorted)
with open("graph_data/graph_full.json", 'w') as fp:
  json.dump(graph, fp)
with open("graph_data/nodes_full.json", 'w') as fp:
  json.dump(nodes, fp)
with open("graph_data/edges_full.json", 'w') as fp:
  json.dump(edges, fp)
with open("graph_data/attribute.json", 'w') as fp:
  json.dump(attribute_value, fp)

print "\nRUNTIME RESULTS:"
print "Number of nodes: "+str(num_of_nodes)
for t in threads:
  print "THREAD "+t.name+" finished with runtime " + str(t.runtime)

time_end = datetime.datetime.now()
full_runtime = time_end - time_start
print "Program finished with runtime " + str(full_runtime)
