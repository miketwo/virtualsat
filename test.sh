#!/bin/bash

docker build -t testcontainer -f Dockerfile.sat . 
docker run --rm -it -v $(pwd):/app --entrypoint "" testcontainer /usr/bin/make test