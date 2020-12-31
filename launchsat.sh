#!/bin/bash

docker build -t satellite -f Dockerfile.sat . 
docker run --rm -it \
	-v $(pwd):/app  \
	-p 5001:5001/tcp \
	satellite
