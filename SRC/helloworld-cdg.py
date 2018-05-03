from pyspark import *
from pyspark.sql import SQLContext
from graphframes import *

conf = SparkConf().setAppName("ta_wira")
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)

# Vertex DataFrame
v = sqlContext.createDataFrame([
  ("r1", 4, 5),
  ("r2", 3, 3),
  ("r3", 7, 3),
  ("r4", 3, 5),
  ("r5", 5, 1),
  ("r6", 5, 4),
  ("r7", 1, 4),
  ("r8", 2, 2),
  ("r9", 2, 5),
  ("r10", 3, 7)
], ["id", "x", "y"])
# Edge DataFrame
e = sqlContext.createDataFrame([
  ("r2", "r3", "dominate"),
  ("r2", "r4", "dominate"),
  ("r2", "r6", "dominate"),
  ("r4", "r1", "dominate"),
  ("r4", "r10", "dominate"),
  ("r5", "r3", "dominate"),
  ("r5", "r6", "dominate"),
  ("r7", "r9", "dominate"),
  ("r7", "r6", "dominate"),
  ("r8", "r2", "dominate"),
  ("r8", "r9", "dominate"),
  ("r9", "r4", "dominate")
], ["src", "dst", "relationship"])
# Create a GraphFrame
g = GraphFrame(v, e)

# Search from "Esther" for users of age < 32.
paths = g.bfs("id = 'r7'", "id = 'r1'")
paths.show()
