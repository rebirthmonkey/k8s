# metric-server

## Installation

```bash
kubectl apply -f components.yaml
kubectl get hpa 
```

> 非常可能需要替换`components.yaml`中k8s.gcr.io源下的镜像。可选方案是`bitnami/metrics-server`
