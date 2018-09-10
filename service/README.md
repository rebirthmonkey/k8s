# Service & Endpoint
## Service
A service routes traffic across a set of pods.
- targetPort: port exposed by pods. if targetPort is not present, it supposed to be the same as port. 
- port: port exposed by services
- nodeIP: IP of the physical server
- pod IP: created be Docker engine
- cluster IP: create by k8s service

- Network Mode
  - clusterIP: 
  - nodePort: 

CMD
- `kubectl get svc`: list services
- `kubectl describe svc SVC_ID`: describe a service
- `kubectl expose deployment DPL_ID --type NodePort --port 8080`: create a service (expose a deployment)
  - `curl CLUSTER_IP`: test
- `kubectl create -f svc1.yaml`: create a service from a YAML file
- `kubectl delete svc SVC_ID`
  - `kubectl delete svc -l name=label`: delete a service by label


## Endpoints
Use endpoints *without label-selector* to connect to an external service
- `kubectl get ep`: list
- `kubectl descrbe ep svc1`: ep use the same name as svc


## Headless Service
*Without clusterIP*, it maps directly to pod endpoints.
It uses only label selector to return backend endpoint list.  
- `kubectl create -f svc-headless.yaml`
- `kubectl describe svc svc-headless`


## Example
### ClusterIP
- `kubectl create -f svc1.yaml`
- `kubectl get svc`: get the clusterIP and port of the service
- `ping CLUSTER_IP`: *cannot ping the CLUSTER_IP*
- `curl CLUSTER_IP:port`: *can curl, ping clusterIP doesnt' work, clusterIP should be bind with port*
  
### NodePort
- `kubectl expose deployment DEP_ID --type NodePort --target-port=pod_port --port=srv_port`: create a service from CMD
- `kubectl get service`: get the random node_port
- `kubectl create -f svc2.yaml`: create a service from a YAML file
- `curl NODE_IP:node_port`: test
