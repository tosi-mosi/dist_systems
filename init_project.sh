#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Usage: init_project.sh <number_of_secondaries>" >&2
  exit 1
fi

docker run -it --rm -uroot -v$(pwd):/root/dist_systems -w/root/dist_systems -p8080:8080 python:3 /bin/bash -c "pip install aiohttp grpcio-tools grpcio && exec /bin/bash -i" \
-name dist_systems.m

docker run -it --rm -uroot -v$(pwd):/root/dist_systems -w/root/dist_systems --ip 192.168.16.3 -p8081:8081 python:3 /bin/bash -c "pip install aiohttp grpcio-tools grpcio && exec /bin/bash -i" \
-name dist_systems.s.1

for (( i=1; i <= $1; ++i ))
do
    docker run -it --rm -uroot -v$(pwd):/root/dist_systems -w/root/dist_systems -p8080:8080 python:3 /bin/bash -c "pip install aiohttp;exec /bin/bash -i" \
-name dist_systems.s.$1
done

# python -m grpc_tools.protoc -I./ --python_out=./ --grpc_python_out=./ rpc.proto

apt-get update && apt-get install -y iproute2
apt-get update && apt-get install -y inetutils-ping

#-p8080:8080 - looks like need it only to have access from host's localhost
#without it can access API through containers IP
docker run -it --rm -uroot -v$(pwd):/root/dist_systems -w/root/dist_systems python:3 /bin/bash \
-c "apt-get update && apt-get install -y inetutils-ping iproute2 && pip install aiohttp grpcio-tools grpcio && exec /bin/bash -i" \
-name dist_systems.m

docker run -it --rm -uroot -v$(pwd):/root/dist_systems -w/root/dist_systems --ip 192.168.16.3 python:3 /bin/bash \
-c "apt-get update && apt-get install -y inetutils-ping iproute2 && pip install aiohttp grpcio-tools grpcio && exec /bin/bash -i" \
-name dist_systems.s