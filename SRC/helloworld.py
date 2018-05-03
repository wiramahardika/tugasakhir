from pyspark import *
from pyspark.sql import SQLContext
from graphframes import *

conf = SparkConf().setAppName("ta_wira")
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)

# Vertex DataFrame
v = sqlContext.createDataFrame([
  ("a", "Alice", 34),
  ("b", "Bob", 36),
  ("c", "Charlie", 30),
  ("d", "David", 29),
  ("e", "Esther", 32),
  ("f", "Fanny", 36),
  ("g", "Gabby", 60)
], ["id", "name", "age"])
# Edge DataFrame
e = sqlContext.createDataFrame([
  ("a", "b", "friend"),
  ("b", "c", "follow"),
  ("c", "b", "follow"),
  ("f", "c", "follow"),
  ("e", "f", "follow"),
  ("e", "d", "friend"),
  ("d", "a", "friend"),
  ("a", "e", "friend")
], ["src", "dst", "relationship"])
# Create a GraphFrame
g = GraphFrame(v, e)

# Search from "Esther" for users of age < 32.
paths = g.bfs("name = 'Esther'", "age = 30")
paths.show()

# # Specify edge filters or max path lengths.
# g.bfs("name = 'Esther'", "age < 32",\
#   edgeFilter="relationship != 'friend'", maxPathLength=3).show()
