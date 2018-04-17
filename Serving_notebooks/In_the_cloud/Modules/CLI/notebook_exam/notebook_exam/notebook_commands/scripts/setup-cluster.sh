#!/bin/bash

NUMBER_OF_WORKERS=$1
FLAVOR=$2
echo $BASH_SOURCE
echo "Setting up $NUMBER_OF_WORKERS workers"

for (( i=1; i<=$NUMBER_OF_WORKERS; i++ ))
	do
		$(dirname $0)/setup-worker.sh worker-$i $FLAVOR &
	done
