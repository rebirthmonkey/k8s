# svc1

## Build
```bash
docker build -t wukongsun/nginx-ingress-demo-svc1:0.1 .
```

## Docker Test
```bash
docker run -d -p 30888:8080 wukongsun/nginx-ingress-demo-svc1:0.1
curl http://localhost:30888
```