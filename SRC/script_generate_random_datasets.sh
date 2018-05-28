#!/bin/bash
rm -rf datasets/independent/*
python generate_random_datasets.py 10000 2
python generate_random_datasets.py 30000 2
python generate_random_datasets.py 50000 2
python generate_random_datasets.py 100000 2
python generate_random_datasets.py 200000 2
python generate_random_datasets.py 10000 3
python generate_random_datasets.py 30000 3
python generate_random_datasets.py 50000 3
python generate_random_datasets.py 100000 3
python generate_random_datasets.py 200000 3
python generate_random_datasets.py 10000 5
python generate_random_datasets.py 30000 5
python generate_random_datasets.py 50000 5
python generate_random_datasets.py 100000 5
python generate_random_datasets.py 200000 5
python generate_random_datasets.py 10000 7
python generate_random_datasets.py 30000 7
python generate_random_datasets.py 50000 7
python generate_random_datasets.py 100000 7
python generate_random_datasets.py 200000 7
python generate_random_datasets.py 10000 10
python generate_random_datasets.py 30000 10
python generate_random_datasets.py 50000 10
python generate_random_datasets.py 100000 10
python generate_random_datasets.py 200000 10
