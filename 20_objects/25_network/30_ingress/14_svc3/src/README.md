# svc1

## Test Code

```bash
go run main.go
curl http://localhost:8080 # in another terminal
```

## Build

```bash
go mod init main
docker build -t wukongsun/nginx-ingress-demo-svc3:0.1 .
```

## Docker Test

```bash
docker run -d -p 30888:8080 wukongsun/nginx-ingress-demo-svc3:0.1
curl http://localhost:30888
```

## k8s Test

```bash
kubectl apply -f service-node-port.yaml
curl http://localhost:30888
kubectl delete -f service-node-port.yaml
```
