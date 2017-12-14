#!/bin/bash

gcloud compute instances stop $1
gcloud compute instances set-machine-type $1 --custom-cpu $2 --custom-memory $3
gcloud compute instances start $1
docker-machine regenerate-certs --force $1