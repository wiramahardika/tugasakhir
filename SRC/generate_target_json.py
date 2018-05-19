import json
import sys

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

def dump_to_file():
    with open("target.json", 'w') as fp:
      json.dump(graph, fp)

def generick_target(attribute_value):
    target = basic_target()
    attr_idx = 0
    for attr in attribute_value:
        t["attr_"+str(attr_idx)] = attr
        attr_idx+=1
    return target

def custom_target():
    return

if len(sys.argv) > 1:
    target = generick_target(sys.argv[1:])
else:
    custom_target()
