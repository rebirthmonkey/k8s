# Basic
## Cluster
- cluster: 1 master + n nodes
- master: a VM or a physical machine which coordinates the cluster
- node/worker: a VM or a physical machine which serves as a worker that runs applications
- namespace: virtual cluster for resource isolation

CMD
- `kubectl cluster-info`
- `kubectl get nodes -o yaml`: -o output format
- `kubectl describe node minikube`: detail about a node
- `kubectl proxy`: create a proxy, all request to `localhost:8001` will be requested to *api-server*
  - `curl http://localhost:8001/version`: test
- `kubectl get namespaces`: list namespaces
- `kubectl --namespace=NS_ID get pods`: execute CMD within 1 namespace


## Metadata
### Label
Labels are key-value pairs that are used to group together sets of objects, very often pods.
- `kubectl get pods --show-labels`: show labels
- `kubectl label pod POD_ID app=v1`: add a label
- `kubectl get pods -l run=kubernetes-bootcamp`: select with label `run=kubernetes-bootcamp`
- `kubectl get services -l run=kubernetes-bootcamp`: select with label `run=kubernetes-bootcamp`

### Annotation
Annotations let you associate arbitrary metadata with k8s objects. 


### Log
- `kubectl logs RESOURCE_ID`: logs


## Object Resources
- [Pod](pod/README.md)
- [ReplicaSet, Deployment, DaemonSet, StatefulSet](deployment/README.md)
- [Service](service/README.md)
- [Storage including Volume, Persistent Volume/ PVC, ConfigMap, Secret](storage/README.md)
- [Network including Ingress](network/README.md)


## Port
- pod
  - containerPort: Docker image/container's exposed port
- service
  - targetPort: *pod's containerPort*
  - port: service's port, clusterIP's port. If not specified, use the same as targetPort 
  - nodePort: node's exposed port for the service