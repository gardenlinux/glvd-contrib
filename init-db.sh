#!/bin/bash

# Quick and dirty script to apply a new db dump to the glvd instance
# Obtain image digest from https://github.com/gardenlinux/glvd-contrib/actions/workflows/pg-init.yaml

if [[ "$#" -ne 1 ]]; then
	echo "Usage: $(basename "$0") <image-digest-sha>"
	exit 1
fi

SHA=$1

kubectl scale --replicas=0 deploy/glvd
kubectl delete po/init-pg
DB_PASSWORD=$(kubectl get secret/postgres-credentials --template="{{.data.password}}" | base64 -d)
kubectl run init-pg --image=ghcr.io/gardenlinux/glvd-postgres-init:latest@sha256:"$SHA" --restart=Never --env=PGHOST=glvd-database-0.glvd-database --env=PGPASSWORD="$DB_PASSWORD"
sleep 40
kubectl logs po/init-pg
sleep 10
kubectl scale --replicas=1 deploy/glvd
