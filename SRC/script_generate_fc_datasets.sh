#!/bin/bash
rm -rf datasets/forest_cover/*
python convert_fc.py 10000 2
python convert_fc.py 30000 2
python convert_fc.py 50000 2
python convert_fc.py 100000 2
python convert_fc.py 200000 2
python convert_fc.py 10000 3
python convert_fc.py 30000 3
python convert_fc.py 50000 3
python convert_fc.py 100000 3
python convert_fc.py 200000 3
python convert_fc.py 10000 5
python convert_fc.py 30000 5
python convert_fc.py 50000 5
python convert_fc.py 100000 5
python convert_fc.py 200000 5
python convert_fc.py 10000 7
python convert_fc.py 30000 7
python convert_fc.py 50000 7
python convert_fc.py 100000 7
python convert_fc.py 200000 7
python convert_fc.py 10000 10
python convert_fc.py 30000 10
python convert_fc.py 50000 10
python convert_fc.py 100000 10
python convert_fc.py 200000 10
