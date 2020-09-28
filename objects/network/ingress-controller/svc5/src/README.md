# svc5

```bash
docker build -t wukongsun/nginx-ingress-demo-svc5:0.1 .
```

## Docker Test
```bash
docker run -d -p 30888:8080 wukongsun/nginx-ingress-demo-svc5:0.1
curl --key ./server.key --cert ./server.crt https://127.0.0.1:30888 -k
```

## ks8 Test
```bash
kubectl apply -f service-node-port.yaml
curl --key ./server.key --cert ./server.crt https://127.0.0.1:30888 -k
```
