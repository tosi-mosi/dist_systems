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

#--------COMPILING GRPC TO PYTHON--------------
# python -m grpc_tools.protoc -I./ --python_out=./ --grpc_python_out=./ rpc.proto

#--------STARTING MASTER AND SECONDARIES--------------
#-p8080:8080 - looks like need it only to have access from host's localhost
#without it can access API through containers IP
#--ip doesn't work as expected
#-eGRPC_VERBOSITY=DEBUG -eGRPC_TRACE=http \
docker run -it --rm -uroot -v$(pwd):/root/dist_systems -w/root/dist_systems --cap-add=NET_ADMIN --net=my_network1 --name dist_systems.m python:3 /bin/bash \
-c "apt-get update && apt-get install -y inetutils-ping iproute2 netcat && pip install aiohttp grpcio-tools grpcio && exec /bin/bash -i"

docker run -it --rm -uroot -v$(pwd):/root/dist_systems -w/root/dist_systems --cap-add=NET_ADMIN --net=my_network1 --name dist_systems.s.1 python:3 \
/bin/bash \
-c "apt-get update && apt-get install -y inetutils-ping iproute2 netcat && pip install aiohttp grpcio-tools grpcio && exec /bin/bash -i"

docker run -it --rm -uroot -v$(pwd):/root/dist_systems -w/root/dist_systems --cap-add=NET_ADMIN --net=my_network1 --name dist_systems.s.2 python:3 \
/bin/bash \
-c "apt-get update && apt-get install -y inetutils-ping iproute2 netcat && pip install aiohttp grpcio-tools grpcio && exec /bin/bash -i"

#for sending requests using dns names
docker run -it --rm -uroot --cap-add=NET_ADMIN --net=my_network1 python:3 \ 
/bin/bash -c "apt-get update && apt-get install -y inetutils-ping iproute2 netcat && exec /bin/bash -i"


#--------DELAYS USING LINUX CMD--------------
# delay is x3 for client->master->sec
# and x2 for client->sec
 docker exec -it dist_systems.s tc qdisc add dev eth0 root netem delay 1s
 docker exec -it dist_systems.s tc qdisc del dev eth0 root
 docker exec -it dist_systems.s tc qdisc show  dev eth0

# for testing
alias lm='time curl dist_systems.m:8080/list';
alias ls1='time curl dist_systems.s.1:8080/list';
alias ls2='time curl dist_systems.s.2:8080/list'
