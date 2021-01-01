#!/bin/bash

docker build -t console -f Dockerfile.console .
docker run --rm -it --link sat console
