# dist_systems
curl dist_systems.m:8080/append -d'{"msg":"msg1","w":"3"}'
curl dist_systems.m:8080/list
curl dist_systems.s.1:8080/list

To start secondary with sleep delay inside gRPC request handler:
./secondary [delay_in_seconds]

./master <number_of_secondaries>