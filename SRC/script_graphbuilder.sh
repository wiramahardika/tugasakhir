#!/bin/bash
python graph_builder.py 500000 50 30000_2,$1
python graph_builder.py 500000 50 10000_3,$1
python graph_builder.py 500000 50 30000_3,$1
python graph_builder.py 500000 50 50000_3,$1
python graph_builder.py 500000 50 100000_3,$1
python graph_builder.py 500000 50 200000_3,$1
python graph_builder.py 500000 50 30000_5,$1
python graph_builder.py 500000 50 30000_7,$1
python graph_builder.py 500000 50 30000_10,$1
