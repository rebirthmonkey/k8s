# k8s Key Components

Kubernetes 主要由以下几个核心组件组成：

Master：

- etcd 保存了整个集群的状态；
- kube-apiserver 提供了资源操作的唯一入口，并提供认证、授权、访问控制、API 注册和发现等机制；
- kube-controller-manager 负责维护集群的状态，比如故障检测、自动扩展、滚动更新等；
- kube-scheduler 负责资源的调度，按照预定的调度策略将 Pod 调度到相应的机器上；

Node：

- kubelet 负责维持容器的生命周期，同时也负责 Volume（CVI）和网络（CNI）的管理；
- Container runtime 负责镜像管理以及 Pod 和容器的真正运行（CRI），默认的容器运行时为 Docker；
- kube-proxy 负责为 Service 提供 cluster 内部的服务发现和负载均衡；

除了核心组件，还有一些推荐的 Add-ons：

- kube-dns 负责为整个集群提供 DNS 服务
- Ingress Controller 为服务提供外网入口
- Heapster 提供资源监控
- Dashboard 提供 GUI
- Federation 提供跨可用区的集群
- Fluentd-elasticsearch 提供集群日志采集、存储与查询

![image-20200806173918737](figures/image-20200806173918737.png)


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