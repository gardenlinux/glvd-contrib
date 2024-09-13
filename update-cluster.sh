#!/bin/bash

# very hacky, surely there is a better way to do this..

podman pull -q --arch=amd64 ghcr.io/gardenlinux/glvd-postgres:edgefulldata
IMAGE=$(podman inspect --format='{{index .RepoDigests 0}}' ghcr.io/gardenlinux/glvd-postgres:edgefulldata)
kubectl set image sts/glvd-database glvd-postgres=$IMAGE

podman pull -q --arch=amd64 ghcr.io/gardenlinux/glvd-api:edge
IMAGE=$(podman inspect --format='{{index .RepoDigests 0}}' ghcr.io/gardenlinux/glvd-api:edge)
kubectl set image deploy/glvd glvd-api=$IMAGE

podman pull -q --arch=arm64 ghcr.io/gardenlinux/glvd-postgres:edgefulldata
podman pull -q --arch=arm64 ghcr.io/gardenlinux/glvd-api:edge
