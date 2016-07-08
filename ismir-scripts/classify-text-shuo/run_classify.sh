#!/bin/bash

for i in {1..10}

do
	echo $i
	python main.py dataset >> results.txt
done