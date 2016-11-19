#!/bin/bash

./downloadSources.sh
split -d -n l/64 data/genres.list data/genres.list.

for i in {00..63}; do
	python dataCombine.py data/genres.list."$i" > results/movies.tsv.$i &
done
