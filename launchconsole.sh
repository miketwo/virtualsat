#!/bin/bash

docker build -t console -f Dockerfile.console .
docker run --rm -it \
    -v $(pwd):/app  \
    --name console \
    --link sat \
    console
