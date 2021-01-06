#!/bin/bash

docker build -t satellite -f Dockerfile.sat .
docker network create VirtualSatNet

if [[ "$1" == "orbit" ]]
then
    docker run --rm -it \
      -p 5001:5001/tcp \
      --name sat \
      --network VirtualSatNet \
      -e USE_ORBIT_PARAMETERS=TRUE \
      satellite
else
    docker run --rm -d \
    	--name sat \
    	--network VirtualSatNet \
    	satellite
fi


