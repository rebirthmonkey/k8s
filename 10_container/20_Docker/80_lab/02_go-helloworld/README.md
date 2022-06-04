# GO App

## Lab

- build image: 
```shell
docker image build -t go-helloworld:0.1 .
```

- run the docker:
```shell
docker run --name go-app -d -p 8888:8080 go-helloworld:0.1
```

- check:
```shell
curl -X GET http://127.0.0.1:8888/hello 
```