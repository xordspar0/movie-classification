#!/bin/bash

./downloadSources.sh

for i in {1..64}; do
	python dataCombine.py $(($i * 10000)) 10000 > results/movies.tsv.$i
done
