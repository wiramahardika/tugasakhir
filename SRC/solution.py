import json
import glob
import sys


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
            if graph[node]["parent"] >= min_subs:
                return [node]
            child = [d['to'] for d in edges if d['from'] == node]
    for next in child:
        cut += find_new_clean_cut(graph, next, min_subs, edges, attribute)
    return cut

expected_subs = int(sys.argv[1])
with open('graph_data/countsubs_results.json') as f:
    countsubs_results = dict(json.load(f))
with open('graph_data/edges_full.json') as f:
    edges = list(json.load(f))
with open('graph_data/attribute.json') as f:
    attribute = list(json.load(f))
with open('graph_data/graph_full.json') as f:
    graph = dict(json.load(f))
with open('graph_data/clean_cut_layer.json') as f:
    clean_cut_layer = dict(json.load(f))
layer_indices = clean_cut_layer.keys()
layer_indices = sorted(map(int, layer_indices))
layer = str([l for l in layer_indices if l <= expected_subs][-1])
node_visited = list()
new_clean_cut = find_new_clean_cut(graph, False, expected_subs, edges, attribute, clean_cut_layer[layer], True)
for new in new_clean_cut:
    print new
    for attr in attribute:
        print attr,":",graph[new][attr]
    print "subscribers :",graph[new]["parent"]
    print "\n"
