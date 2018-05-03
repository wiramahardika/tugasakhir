import random
import datetime

def generate_vertex(v):
  result = {}
  for n in range(v):
    id = 'r'+str(n+1)
    result[id] = {
      "x": random.randint(1,500),
      "y": random.randint(1,500),
      "visited": False,
      "child": []
    }
  return result

def example_vertex():
  v = {
    "r1": {
      "x": 4,
      "y": 5,
      "visited": False,
      "child": []
    },
    "r2": {
      "x": 3,
      "y": 3,
      "visited": False,
      "child": []
    },
    "r3": {
      "x": 7,
      "y": 3,
      "visited": False,
      "child": []
    },
    "r4": {
      "x": 3,
      "y": 5,
      "visited": False,
      "child": []
    },
    "r5": {
      "x": 5,
      "y": 1,
      "visited": False,
      "child": []
    },
    "r6": {
      "x": 5,
      "y": 4,
      "visited": False,
      "child": []
    },
    "r7": {
      "x": 1,
      "y": 4,
      "visited": False,
      "child": []
    },
    "r8": {
      "x": 2,
      "y": 2,
      "visited": False,
      "child": []
    },
    "r9": {
      "x": 2,
      "y": 5,
      "visited": False,
      "child": []
    },
    "r10": {
      "x": 3,
      "y": 7,
      "visited": False,
      "child": []
    }
  }
  return v

def remove_from_list(origin, to_remove):
  temp = set(to_remove)
  result = [value for value in origin if value not in to_remove]
  return result

def merge(first_list, second_list):
  return first_list + list(set(second_list) - set(first_list))

def is_dominating(subject, target):
  if subject["x"] <= target["x"] and subject["y"] <= target["y"]:
    return True
  else:
    return False

def is_dominated(target, subject):
  if target["x"] >= subject["x"] and target["y"] >= subject["y"]:
    return True
  else:
    return False

def is_skyline(target, set):
  global count
  skyline_cand = list(set)
  for candidate in skyline_cand:
    count+=1
    if target is candidate:
      continue
    elif is_dominated(vertex[target], vertex[candidate]):
      return False
  return True

def find_skyline(set):
  skyline_cand = list(set)
  result = []
  for record in skyline_cand:
    if is_skyline(record, skyline_cand):
      result.append(record)
  return result

def find_dominating(r, set):
  result = []
  for s in set:
    if r is s:
      continue
    elif is_dominating(vertex[r], vertex[s]):
      result.append(s)
  return result

def progress_report(node):
  global node_visited
  global num_of_nodes
  node_visited = merge(node_visited, [node])
  progress = float(len(node_visited))/float(num_of_nodes)*float(100)
  return "Number of visited nodes: " + str(len(node_visited)) + " of " + str(num_of_nodes) + " nodes --- " + str(progress) + "%"

def build_graph(node, layer, is_initial = False):
  if not is_initial:
    print "Entering node " + node
    if vertex[node]["visited"]:
      print "Building graph returned because node " + node + " has been visited before"
      return
    else:
      vertex[node]["visited"] = True
      print progress_report(node)
  else:
    print "Entering initial node"

  if len(layer) <= 1:
    print "Building graph returned because node " + node + " is leaf"
    return

  child = find_skyline(layer)
  layer_cand = remove_from_list(list(layer), child)

  if not is_initial:
    vertex[node]["child"] = child
    print node + "'s next node is:"
    print child

  for record in child:
    new_layer = find_dominating(record, layer_cand)
    print "Layer restricted for " + record
    build_graph(record, new_layer)

  return

time_start = datetime.datetime.now()
print "Program started"
count = 0
node_visited = []
num_of_nodes = 100000

vertex = generate_vertex(num_of_nodes)
# vertex = example_vertex()

build_graph(None, vertex.keys(), True)
print vertex

time_end = datetime.datetime.now()
full_runtime = time_end - time_start
print "Program finished with runtime " + str(full_runtime)
print "Find skyline loop count: " + str(count)
