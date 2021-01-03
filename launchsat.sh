#!/bin/bash

docker build -t satellite -f Dockerfile.sat . 
docker network create VirtualSatNet
docker run --rm -it \
	-p 5001:5001/tcp \
	--name sat \
	--network VirtualSatNet \
	satellite
