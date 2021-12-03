# Network

## 简介

### 网络模型

k8s的网络模型如下：

- IP-per-Pod，每个 Pod 都拥有一个独立 IP 地址，Pod 内所有容器共享一个网络命名空间
- 集群内所有 Pod 都在一个直接连通的扁平网络中，可通过 IP 直接访问
  - 所有容器之间无需 NAT 就可以直接互相访问
  - 所有 Node 和所有容器之间无需 NAT 就可以直接互相访问
  - 容器自己看到的 IP 跟其他容器看到的一样
- Service cluster IP 尽可在集群内部访问，外部请求需要通过 NodePort、LoadBalance 或者 Ingress 来访问

### 网络类型

#### hostPort（Pod-Level）

hostPort相当于`docker run -p 30890:80`，为容器在主机上做个NAT映射，不用创建svc，因此端口只在容器运行的vm上监听。但是其缺点是无法负载多pod，具体实例见[pod1-host-port.yaml](pod1-host-port.yaml)

```bash
curl localhost:3089
```

#### hostNetwork（Pod-Level）

hostNetwork相当于`docker run --net=host`，与主机共享network网络栈，不用创建svc，因此端口只在容器运行的vm上监听。但是其缺点是无法负载多pod，具体实例见[pod2-host-network.yaml](pod2-host-network.yaml)

#### NodePort（Service-Level）

由kube-proxy操控为所有节点统一配置iptables规则。因此，svc上的nodeport会监听在所有的节点上。即使有1个pod，访问任意节点的nodeport都可以访问到这个服务。

具体实例见[service1-node-port.yaml](service1-node-port.yaml)

#### externalIPS（Service-Level）

通过svc来实现pod间的负载，但要求只监听某台指定node上，而非像nodeport那样监听所有节点。

具体实例见[service2-external-ip.yaml](service2-external-ip.yaml)

## Ingress Controller

- [Ingress Controller](ingress-controller/README.md)



