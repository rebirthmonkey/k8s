# svc3

```bash
docker build -t wukongsun/nginx-ingress-demo-svc3:0.1 .
```

## Docker Test
```bash
docker run -d -p 30888:8080 wukongsun/nginx-ingress-demo-svc3:0.1
curl http://localhost:30888
```

## ks8 Test
```bash
kubectl apply -f service-node-port.yaml
curl http://localhost:30888
```

