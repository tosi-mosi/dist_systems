# dist_systems
time curl -X POST http://192.168.16.2:8080/append -d"msg1"
time curl -X GET http://localhost:8080/list

time curl -X POST http://192.168.16.2:8080/append -d"msg1"
time curl -X GET http://192.168.16.2:8080/list

time curl -X GET http://192.168.16.3:8080/list

To start secondary with sleep delay inside gRPC request handler:
python3 Secondary.py <delay_in_seconds>