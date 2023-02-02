#!/usr/bin/env bash

set -ex

mkdir -p data/ # All matrices are in here

cd data/ && python3 inst_gen.py -S 4 -t 7 -n 2 && cd ..

python3 main.py
