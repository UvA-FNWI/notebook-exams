#!/bin/bash

NUMBER_OF_WORKERS=$1
CPU=$2
MEMORY=$3

echo "Setting up $NUMBER_OF_WORKERS workers"

for (( i=2; i<=$NUMBER_OF_WORKERS; i++ ))
	do
		echo "Scaling worker-$i"
		./scale-worker.sh worker-$i $CPU $MEMORY &
	done