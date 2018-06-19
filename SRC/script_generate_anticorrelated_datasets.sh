#!/bin/bash
rm -rf datasets/anti_correlated/*
python generate_anticorrelated_datasets.py 30000 2
python generate_anticorrelated_datasets.py 10000 3
python generate_anticorrelated_datasets.py 30000 3
python generate_anticorrelated_datasets.py 50000 3
python generate_anticorrelated_datasets.py 100000 3
python generate_anticorrelated_datasets.py 200000 3
python generate_anticorrelated_datasets.py 30000 5
python generate_anticorrelated_datasets.py 30000 7
python generate_anticorrelated_datasets.py 30000 10
