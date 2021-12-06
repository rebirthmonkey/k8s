# svc6

```bash
docker build -t wukongsun/nginx-ingress-demo-svc6:0.1 .
```

## Docker Test
```bash
docker run -d -p 30888:8080 wukongsun/nginx-ingress-demo-svc6:0.1
telnet 127.0.0.1 30888
```

## ks8 Test
```bash
kubectl apply -f service-node-port.yaml
telnet 127.0.0.1 30888
```

