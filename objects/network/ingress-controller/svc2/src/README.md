# svc2

```bash
docker build -t wukongsun/nginx-ingress-demo-svc2:0.1 .
```

## Docker Test
```bash
docker run -d -p 30888:8080 wukongsun/nginx-ingress-demo-svc2:0.1
curl -k https://localhost:30888
```

## ks8 Test
```bash
kubectl apply -f service-node-port.yaml
curl -k https://localhost:30888
```