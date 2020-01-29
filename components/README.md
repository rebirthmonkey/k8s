# k8s Key Components
- `API server` encapsulates `etcd` for data manipulation
- `AAA (Authentication, Authorization, Admission Controll)` protects `API server` from `kubectl proxy` and `kubectl` access
- `Controller Manager's Controllers` manipulate resource objects in `etcd` through `API server` independently
- `Scheduler` manipulates resource objects in `etcd` through `API server`
- each `kubelet` get related information from `etcd` through `API server`  

![Kubernetes Architecture](figures/k8s-architecture.png)


## kube-apiserver
- [kube-apiserver](kube-apiserver/README.md)


## kube-controller-manager
- [kube-controller-manager](kube-controller-mgr/README.md)


## kube-scheduler
- [kube-scheduler](kube-scheduler/README.md)


## kubelet
- [kubelet](kubelet/README.md)


## kube-proxy
- [kube-proxy](kube-proxy/README.md)


## kube-dns
- [kube-dns](kube-dns/README.md)


## Security
- [Security](component/aaa/README.md)