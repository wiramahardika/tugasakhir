import json
import glob
import sys
import pprint


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

def calculate_potential_subs(g, clean_cut):
    highest_score = sorted(clean_cut, key=lambda x:(g[x]["score"]), reverse=True)[0]
    return g[highest_score]["score"] + (len(clean_cut)-1)

def calculate_cost(clean_cut, g, attribute):
    new_preference = dict()
    cost = 0
    is_first = True
    for attr in attribute:
        best_sub = sorted(clean_cut, key=lambda x: (g[x][attr]))[0]
        best_value = int(g[best_sub][attr])
        if is_first:
            new_preference[attr] = best_value - 1
        else:
            new_preference[attr] = best_value
        cost += new_preference[attr]
        is_first = False
    return [new_preference, cost]

def generatekey(x):
    results = list()
    for attr in attribute:
        results.append(graph_full[x][attr])
    return tuple(results)

def adjust_cleancut(g_results, nodes, edges, attribute, is_initial = False):
    global itteration
    global comb_record
    if is_initial:
        if g_results["subs_treshold"] == 0:
            return False
        elif g_results["subs_treshold"] == g_results["num_of_nodes"]:
            nodes = {k: v for k, v in g_results["graph"].iteritems() if v["is_root"]}
            return nodes.keys()
        else:
            nodes = g_results["results"]["clean_cut"]
            if len(nodes) < 1:
                nodes = {k: v for k, v in g_results["graph"].iteritems() if len(v["child"]) is 0}
                nodes = nodes.keys()
            if len(nodes) >= g_results["subs_treshold"]:
                return nodes
    else:
        nodes = find_skyline(nodes, g_results["graph"], attribute)
    potential_subs = calculate_potential_subs(g_results["graph"], nodes)
    if potential_subs >= g_results["subs_treshold"]:
        return nodes
    else:
        best_result = {
            "clean_cut": False,
            "preference": False
        }
        for n in nodes:
            p_node = [d for d in edges if d['to'] in [n]]
            p_node = [d['from'] for d in p_node]
            for parent in p_node:
                itteration+=1
                nodes_temp = list(nodes)
                nodes_temp.remove(n)
                nodes_temp.append(parent)
                nodes_temp = sorted(nodes_temp, key=generatekey)
                nodes_temp = find_skyline(nodes_temp, g_results["graph"], attribute)
                if nodes_temp in comb_record:
                    continue
                else:
                    clean_cut_cand = adjust_cleancut(g_results, nodes_temp, edges, attribute)
                    preference_cand = calculate_cost(clean_cut_cand, g_results["graph"], attribute)
                    print clean_cut_cand,preference_cand[1]
                    if not best_result["clean_cut"] or preference_cand[1] > best_result["preference"][1]:
                        best_result["clean_cut"] = clean_cut_cand
                        best_result["preference"] = preference_cand
                    comb_record.append(nodes)
        return best_result["clean_cut"]


# ---------------------- MAIN PROGRAM ----------------------
expected_subs = int(sys.argv[1])
with open('graph_data/countsubs_results.json') as f:
    countsubs_results = dict(json.load(f))
with open('graph_data/edges_full.json') as f:
    edges = list(json.load(f))
with open('graph_data/attribute.json') as f:
    attribute = list(json.load(f))
graph = list()
graph_file = glob.glob('graph_data/graph-*.json')
for gf in graph_file:
    with open(gf) as f:
        g_dict = dict(json.load(f))
    graph.append(g_dict)
with open('graph_data/graph_full.json') as f:
    graph_full = dict(json.load(f))
graph_results = list()
num_of_nodes_tmp = expected_subs
for x in reversed(range(len(countsubs_results["graph_results"]))):
    nodes_max = len(graph[x])
    if num_of_nodes_tmp >= nodes_max:
        graph_subs = nodes_max
        num_of_nodes_tmp -= nodes_max
    else:
        graph_subs = num_of_nodes_tmp
        num_of_nodes_tmp = 0
    graph_results.append({"graph":graph[x], "results":countsubs_results["graph_results"][x], "num_of_nodes":nodes_max, "subs_treshold":graph_subs})
itteration = 0
comb_record = list()
for gr in graph_results:
    print adjust_cleancut(gr, False, edges, attribute, True)
print itteration
