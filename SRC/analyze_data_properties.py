import sys
import csv
import os, shutil
import random
import json


attribute = [
    "id",
    "label",
    "Elevation",
    "Aspect",
    "Slope",
    "Horizontal_Distance_To_Hydrology",
    "Vertical_Distance_To_Hydrology",
    "Horizontal_Distance_To_Roadways",
    "Hillshade_9am",
    "Hillshade_Noon",
    "Hillshade_3pm",
    "Horizontal_Distance_To_Fire_Points",
]
attribute_data = attribute[2:]
data = list()
properties = dict()
vertex = dict()
with open('covtype.data') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        row_used = row[0:10]
        vertex_data = dict()
        for idx in range(len(row_used)):
            vertex_data[attribute_data[idx]] = int(row[idx])
        vertex[row_used[0]] = vertex_data
for attr in attribute_data:
    vertex_min = sorted(vertex, key=lambda x: (vertex[x][attr]))
    properties[attr] = {
        "min": vertex[vertex_min[0]][attr],
        "max": vertex[vertex_min[-1]][attr]
    }
with open("datasets/properties.json", 'w') as fp:
    json.dump(properties, fp)
with open("datasets/attribute.json", 'w') as fp:
    json.dump(attribute, fp)
