import datetime
time_start = datetime.datetime.now()
print "Program started"

import csv
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession

def build_graph():


spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()

attribute = list()
with open('dataset.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        attribute = list(row[2:])
        break

df = spark.read.format("csv").option("header", "true").load("dataset.csv")
df.createOrReplaceTempView("vertex")

cast_sql = "SELECT CAST(id AS int), label"
for i in range(len(attribute)):
    cast_sql += ", CAST("+attribute[i]+" AS int)"
cast_sql += " FROM vertex"

vertex = spark.sql(cast_sql)
vertex.createOrReplaceTempView("vertex")
vertex.show()

target = spark.sql("SELECT * FROM vertex")
target.createOrReplaceTempView("target")

dominance_start = datetime.datetime.now()
dominance_map_sql = "SELECT v.id as this_vertex, t.id as dominating_this_vertex FROM vertex v, target t"
for i in range(len(attribute)):
    if i == 0:
        dominance_map_sql += " WHERE (v."+attribute[i]+" <= t."+attribute[i]
    else:
        dominance_map_sql += " AND v."+attribute[i]+" <= t."+attribute[i]
dominance_map_sql += ") AND"
for i in range(len(attribute)):
    if i == 0:
        dominance_map_sql += " (v."+attribute[i]+" < t."+attribute[i]
    else:
        dominance_map_sql += " OR v."+attribute[i]+" < t."+attribute[i]
dominance_map_sql += ") ORDER BY this_vertex"

dominance_map = spark.sql(dominance_map_sql)
dominance_map.createOrReplaceTempView("dominance_map")
dominance_end = datetime.datetime.now()
dominance_full = dominance_end - dominance_start

layer = spark.sql("SELECT DISTINCT dominating_this_vertex as id FROM dominance_map")
layer.createOrReplaceTempView("layer")

sky_start = datetime.datetime.now()
skyline = spark.sql("SELECT v.id FROM vertex v LEFT JOIN layer l ON v.id = l.id WHERE l.id IS NULL")
sky_end = datetime.datetime.now()
sky_full = sky_end - sky_start

time_end = datetime.datetime.now()
full_runtime = time_end - time_start
print "Program finished with runtime " + str(full_runtime)
print "Dominance mapping finished with runtime " + str(dominance_full)
print "Finding skyline finished with runtime " + str(sky_full)
