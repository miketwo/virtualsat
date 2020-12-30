#!/bin/bash

docker build -t my_container_name . 
docker run --rm -it -v $(pwd):/app my_container_name /usr/bin/make test