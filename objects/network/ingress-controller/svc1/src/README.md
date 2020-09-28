# svc1

## Build
```bash
go mod init main
go test
docker build -t wukongsun/nginx-ingress-demo-svc1:0.1 .
```

## Docker Test
```bash
docker run -d -p 30888:8080 wukongsun/nginx-ingress-demo-svc1:0.1
curl http://localhost:30888
```

## k8s Test
```bash
kubectl apply -f service-node-port.yaml
curl http://localhost:30888
```