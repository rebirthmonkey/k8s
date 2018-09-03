# Service & Headless
## Service
A service routes traffic across a set of pods.
- targetPort: port exposed by pods. if targetPort is not present, it supposed to be the same as port. 
- port: port exposed by services
- nodeIP: IP of the physical server
- pod IP: created be Docker engine
- cluster IP: create by k8s service

### Network Mode
- clusterIP: 
- nodePort: 

### CMD
- `kubectl get services`: list services
- `kubectl get services SVC_ID`: list a service
- `kubectl describe services`: describe services
- `kubectl describe services SVC_ID`: describe a service
- `kubectl expose deployment DEP_ID --type NodePort --port 8080`: create a service (expose a deployment)
  - `curl $(minikube ip):NODE_PORT`: test
- `kubectl create -f service.yaml`: create a service from a YAML file
- `kubectl delete service -l name=label`: delete a service by label

## Endpoints
To integrate external services

```
kind: Endpoints
metadata: 
  name: my-service  # should be the same as the no-label-selector service
  subsets: 
  - addresses: 
    - IP: 1.2.3.4
    ports:
    - port: 80
```

## Headless Service
Without clusterIP, it maps directly to pod endpoints, uses only label selector to return backend endpoint list.  


## TP
### TP1: NodePort
- `kubectl expose deployment DEP_ID --type NodePort --target-port=pod_port --port=srv_port`: create a service from CMD
- `kubectl get service`: get the random node_port
- `kubectl create -f SVC.yaml`: create a service from a YAML file
- `curl $(minikube ip):node_port`: test

### TP2: ClusterIP
- `kubectl create -f SVC.yaml`
- `kubectl get svc`: get the clusterIP and port of the service
- `minikube ssh`: access to the master/node
  - `curl clusterIP:port`: test. *ping clusterIP doesnt' work, clusterIP should be bind with port*