#!/bin/bash

set -ex

mkdir -p data/ # All matrices are in here

cd data/ && python3 inst_gen.py -S 4 -t 7 -n 2 && cd ..

python3 -m venv .venv # Create virtual environment
source .venv/bin/activate
pip install -r requirements.txt && python main.py # Install reqs and run script
