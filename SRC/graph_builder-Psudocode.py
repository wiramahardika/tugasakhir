import random
import datetime
import time
import threading
import json
import sys
import csv
import copy
import os, shutil
import psutil
import resource
FUNCTION format_graph(v_global, node, edges):
    ENDFOR
    root <- find_skyline(node, v_global)
    for x in node:
        score <- len(v_global[x]["ancestor"])
        v_global[x]["score"] <- score+1
        del v_global[x]["ancestor"]
        IF x in root:
            v_global[x]["is_root"] <- True
        ENDIF
ENDFUNCTION

    ENDFOR
FUNCTION format_nodes(v, node):
    ENDFOR
    v_local <- dict(v)
    result <- list()
    for x in range(len(node)):
        v_local[node[x]]["label"] += "\n("
        a_idx <- 0
        for a in attribute_value:
            IF a_idx = 0:
                v_local[node[x]]["label"] += str(v_local[node[x]][a])
            ELSE:
                v_local[node[x]]["label"] += ","+str(v_local[node[x]][a])
            ENDIF
            a_idx+=1
        ENDFOR
        v_local[node[x]]["label"] += ")\n"+str(v_local[node[x]]['score'])
        result.append(v_local[node[x]])
    ENDFOR
    RETURN result
ENDFUNCTION

FUNCTION format_layer(v, node, start_point, edges, attribute, cut_size <- False):
    ENDFOR
    global node_visited
    v_local <- dict(v)
    result <- dict()
    num_of_nodes <- len(node)
    IF not cut_size:
        cut_size <- num_of_nodes/2
    ENDIF
    for layer in range(0,num_of_nodes+1,cut_size):
        result_temp <- search_clean_cut(v_local, False, layer, edges, attribute, start_point, True)
        result_temp <- sorted(result_temp, key=generatekey)
        result_temp <- find_skyline(result_temp, v_local)
        result[layer] <- result_temp
        start_point <- result[layer]
        node_visited <- list()
        IF len(result_temp) < 1:
            del result[layer]
            break
        ENDIF
    ENDFOR
    RETURN result
ENDFUNCTION

FUNCTION search_clean_cut(graph, node, layer_size, edges, attribute, root <- [], is_initial <- False):
    cut <- list()
    clean_cut <- list()
    IF is_initial:
        child <- root
    ELSE:
        IF node in node_visited:
            RETURN list()
        ELSE:
            node_visited.append(node)
            IF graph[node]["score"] >= layer_size:
                RETURN [node]
            ENDIF
            child <- [d['to'] for d in edges IF d['from'] = node]
    ENDIF
        ENDIF
                                            ENDIF
                             ENDFOR
    for next in child:
        cut += search_clean_cut(graph, next, layer_size, edges, attribute)
    ENDFOR
    RETURN cut
ENDFUNCTION

FUNCTION slice_vertex(v, max):
  v_thread <- []
  for x in range(0,len(v),max):
    v_thread.append(v[x:x+max])
  ENDFOR
  RETURN v_thread
ENDFUNCTION

FUNCTION remove_from_list(origin, to_remove):
  temp <- set(to_remove)
  result <- [value for value in origin IF value not in to_remove]
                                      ENDIF
                  ENDFOR
  RETURN result
ENDFUNCTION

FUNCTION merge(first_list, second_list):
  RETURN first_list + list(set(second_list) - set(first_list))
ENDFUNCTION

FUNCTION is_dominating(subject, target):
    dominate <- 0
    for attr in attribute_value:
        IF subject[attr] > target[attr]:
            RETURN False
        ELSEIF subject[attr] < target[attr]:
            dominate+=1
        ENDIF
    ENDFOR
    IF dominate < 1:
        RETURN False
    ELSE:
        RETURN True
    ENDIF
ENDFUNCTION

FUNCTION is_skyline(target, set, v):
  skyline_cand <- list(set)
  for candidate in skyline_cand:
    IF target is candidate:
      continue
    ELSEIF is_dominating(v[candidate], v[target]):
      RETURN False
    ENDIF
  ENDFOR
  RETURN True
ENDFUNCTION

FUNCTION find_skyline(set, v):
  skyline_cand <- list(set)
  result <- []
  i <- 1;
  for record in skyline_cand:
    IF is_skyline(record, skyline_cand[0:i], v):
      result.append(record)
    ENDIF
    i+=1
  ENDFOR
  RETURN result
ENDFUNCTION

FUNCTION find_dominating(r, set, v):
  result <- []
  for s in set:
    IF r is s:
      continue
    ELSEIF is_dominating(v[r], v[s]):
      result.append(s)
    ENDIF
  ENDFOR
  RETURN result
ENDFUNCTION

FUNCTION progress_report(node):
  global node_visited
  global num_of_nodes
  node_visited <- merge(node_visited, [node])
  progress <- float(len(node_visited))/float(num_of_nodes)*float(100)
  process <- psutil.Process(os.getpid())
  sys.stdout.write("\rNumber of visited nodes: " + str(len(node_visited)) + " of " + str(num_of_nodes) + " nodes --- " + str(progress) + "% ("+str(mem_usage)+" MB)")
  sys.stdout.flush()
ENDFUNCTION

FUNCTION generatekey(x):
    results <- list()
    for attr in attribute_value:
        results.append(vertex[x][attr])
    ENDFOR
    RETURN tuple(results)
ENDFUNCTION

FUNCTION build_graph(node, thread_vertex, sub_vertex, is_initial <- False):
    IF not is_initial:
        IF vertex[node]["visited"] OR node not in thread_vertex:
            RETURN
        ELSE:
            child_cand <- list(find_dominating(node, sub_vertex, vertex))
            vertex[node]["visited"] <- True
            for c in child_cand:
                IF node not in vertex[c]["ancestor"]:
                    vertex[c]["ancestor"].append(node)
        ENDIF
                ENDIF
            ENDFOR
    ELSE:
        child_cand <- thread_vertex
    ENDIF
    child <- find_skyline(child_cand, vertex)
    sub_vertex_cand <- remove_from_list(list(child_cand), child)
    IF not is_initial:
        for c in child:
            edge_temp <- dict()
            edge_temp["to"] <- c
            edge_temp["from"] <- node
            edges.append(edge_temp)
        ENDFOR
        progress_report(node)
    ENDIF
    for record in child:
        IF is_initial:
            index_cut <- sub_vertex.index(record)
            build_graph(record, thread_vertex, sub_vertex[index_cut:])
        ELSE:
            build_graph(record, thread_vertex, sub_vertex_cand)
        ENDIF
    ENDFOR
    RETURN
ENDFUNCTION

CLASS cdgThread(threading.Thread):
    FUNCTION __init__(self, threadID, name, thread_vertex, sub_vertex):
        threading.Thread.__init__(self)
         threadID <- threadID
         name <- name
         thread_vertex <- thread_vertex
         sub_vertex <- sub_vertex
    ENDFUNCTION

    FUNCTION run(self):
        OUTPUT "\nTHREAD "+ name+" started"
        build_graph(None,  thread_vertex,  sub_vertex, True)
        t_end <- datetime.datetime.now()
         runtime <- t_end - time_start
        OUTPUT "THREAD "+ name+" finished with runtime " + str( runtime)
    ENDFUNCTION

ENDCLASS

ts <- time.time()
st_start <- datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d__%H:%M:%S')
time_start <- datetime.datetime.now()
OUTPUT "Program started"
count <- 0
node_visited <- []
num_of_nodes <- 0
try:
    max_nodes_in_thread <- int(sys.argv[1])
except IndexError:
    max_nodes_in_thread <- 10000
try:
    cut_size <- int(sys.argv[2])
except IndexError:
    cut_size <- False
try:
    session <- sys.argv[3].split(',')
    session_name <- session[0]
    session_type <- session[1]
    session_full_id <- "_"+session_name+"_"+session_type
except IndexError:
    session <- False
    session_name <- ""
    session_type <- ""
    session_full_id <- ""
vertex <- dict()
attribute <- list()
edges <- list()
IF session:
    dataset_filename <- "datasets/"+session_type+"/dataset_"+session_name+".csv"
ELSE:
    dataset_filename <- "dataset.csv"
ENDIF
with open(dataset_filename) as csvfile:
    readCSV <- csv.reader(csvfile, delimiter=',')
    init <- True
    for row in readCSV:
        IF init:
            attribute <- list(row)
        ELSE:
            vertex_data <- dict()
            for idx in range(len(row)):
                IF idx > 1:
                    vertex_data[attribute[idx]] <- int(row[idx])
                ELSE:
                    vertex_data[attribute[idx]] <- row[idx]
                ENDIF
            ENDFOR
            vertex[row[0]] <- vertex_data
            vertex[row[0]]["score"] <- 0
            vertex[row[0]]["ancestor"] <- list()
            vertex[row[0]]["visited"] <- False
            vertex[row[0]]["is_root"] <- False
            num_of_nodes+=1
        ENDIF
        init <- False
    ENDFOR
attribute_value <- list(attribute[2:])
properties <- dict()
for attr in attribute_value:
    vertex_min <- sorted(vertex, key=lambda x: (vertex[x][attr]))
    properties[attr] <- {
        "min": vertex[vertex_min[0]][attr],
        "max": vertex[vertex_min[-1]][attr]
    }
ENDFOR
vertex_sorted <- sorted(vertex, key=generatekey)
vertex_thread <- slice_vertex(vertex_sorted, max_nodes_in_thread)
threads <- []
for t in range(0,len(vertex_thread)):
    threads.append(cdgThread(t+1,"Graph Builder #"+str(t+1),vertex_thread[t],vertex_sorted))
ENDFOR
for t in threads:
    t.start()
ENDFOR
for t in threads:
    t.join()
ENDFOR
folder <- 'session'+session_full_id
for the_file in os.listdir(folder):
    file_path <- os.path.join(folder, the_file)
    try:
        IF os.path.isfile(file_path):
            os.unlink(file_path)
        ENDIF
    except Exception as e:
        OUTPUT e
ENDFOR
format_graph(vertex, vertex_sorted, edges)
ENDFOR
with open("session"+session_full_id+"/graph.json", 'w') as fp:
    json.dump(vertex, fp)
node_visited <- list()
first_layer_root <- {k: v for k, v in vertex.iteritems() IF v["is_root"]}
                                                        ENDIF
                         ENDFOR
first_layer_root <- first_layer_root.keys()
clean_cut_layer <- format_layer(vertex, vertex_sorted, first_layer_root, edges, attribute_value, cut_size)
                  ENDFOR
with open("session"+session_full_id+"/clean_cut_layer.json", 'w') as fp:
    json.dump(clean_cut_layer, fp)
del clean_cut_layer
nodes <- format_nodes(vertex, vertex_sorted)
        ENDFOR
with open("session"+session_full_id+"/nodes.json", 'w') as fp:
    json.dump(nodes, fp)
del nodes
with open("session"+session_full_id+"/attribute.json", 'w') as fp:
    json.dump(attribute_value, fp)
with open("session"+session_full_id+"/properties.json", 'w') as fp:
    json.dump(properties, fp)
del properties
with open("session"+session_full_id+"/edges.json", 'w') as fp:
    json.dump(edges, fp)
del edges
OUTPUT "\nRUNTIME RESULTS:"
OUTPUT "Number of nodes: "+str(num_of_nodes)
time_end <- datetime.datetime.now()
full_runtime <- time_end - time_start
OUTPUT "Program finished with runtime " + str(full_runtime)
process <- psutil.Process(os.getpid())
OUTPUT "Memory usage:",mem_usage
res <- list()
ts <- time.time()
st_end <- datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d__%H:%M:%S')
res_data <- list()
res_data.append(st_start)
res_data.append(st_end)
res_data.append("algo1")
res_data.append(num_of_nodes)
res_data.append(len(attribute_value))
res_data.append(session_type)
res_data.append(len(threads))
res_data.append(full_runtime)
res_data.append(mem_usage)
res.append(res_data)
IF session:
    with open("session_log/graph_script.csv", "a") as output:
        writer <- csv.writer(output, lineterminator='\n')
        writer.writerows(res)
ELSE:
    with open("session_log/graph_manual.csv", "a") as output:
        writer <- csv.writer(output, lineterminator='\n')
        writer.writerows(res)
