# dist_systems
curl -X POST http://192.168.16.2:8080/append -H"Content-type: application/json" -d"msg1"
curl -X GET http://localhost:8080/list

curl -X POST http://192.168.16.2:8080/append -d"msg1"
curl -X GET http://192.168.16.2:8080/list

curl -X GET http://192.168.16.3:8080/list
