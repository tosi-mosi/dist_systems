# dist_systems
time curl -X POST localhost/append -d"msg1"
time curl -X GET localhost/list

To start secondary with sleep delay inside gRPC request handler:
./secondary [delay_in_seconds]

./master <number_of_secondaries>