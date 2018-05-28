#!/bin/bash
rm session_log/$1_$2.csv
cp session_log/$1.csv.backup session_log/$1_$2.csv
