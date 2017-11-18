#!/bin/bash

LABEL=$1
NUMBER_OF_WORKERS=$2
FLAVOR=$3

echo "Setting up $NUMBER_OF_WORKERS workers"

for (( i=1; i<=$NUMBER_OF_WORKERS; i++ ))
	do
		./setup-worker.sh worker-$LABEL-$i $FLAVOR &
	done