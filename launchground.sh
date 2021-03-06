#!/bin/bash

docker build -t groundstation -f Dockerfile.gs .
docker network create VirtualSatNet
docker run --rm -it \
    -v $(pwd):/app  \
    -p 5000:5000/tcp \
    --name gs \
    --network VirtualSatNet \
    groundstation
