#!/bin/bash

docker build -t console -f Dockerfile.console .
docker network create VirtualSatNet
docker run --rm -it \
    -v $(pwd):/app  \
    --name console \
    --network VirtualSatNet \
    console
