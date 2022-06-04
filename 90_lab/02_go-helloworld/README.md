# GO App

## Lab
based on the previous Docker/lab/02_go-helloworld app

- run k8s deployment and service:
```shell
kubectl apply -f helloworld.yaml
```

- check:
```shell
curl -X GET http://127.0.0.1:30080/hello
```

