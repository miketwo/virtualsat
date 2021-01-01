#!/bin/bash

docker build -t satellite -f Dockerfile.sat . 
docker run --rm -it \
	-p 5001:5001/tcp \
	--name sat \
	satellite
