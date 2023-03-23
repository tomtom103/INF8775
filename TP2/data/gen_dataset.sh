#!/bin/bash

# Pour glouton et approx
for n in {"5","10","15","20","50","100","250","500","750","1000","1250"}; do
    ./inst_gen.py -s $n -n 5
done

# Pour tous les algorithmes
for n in {"5","10","15","20"}; do
    ./inst_gen.py -s $n -n 5 -x DP
done
