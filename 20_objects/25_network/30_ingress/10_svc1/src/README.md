# svc1

## Test Code

```shell
go run main.go
curl http://localhost:8080 # in another terminal
```

## Build

```shell
go mod init main
go mod tidy
docker build -t wukongsun/nginx-ingress-demo-svc1:0.1 .
docker push wukongsun/nginx-ingress-demo-svc1:0.1
```

## Docker Test

```shell
docker run -d -p 30888:8080 wukongsun/nginx-ingress-demo-svc1:0.1
curl http://localhost:30888
```

## k8s Test

```shell
kubectl apply -f service-node-port.yaml
curl http://localhost:30888
```
