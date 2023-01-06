# Network

## 简介

### 网络模型

k8s的网络模型特点如下：

- IP-per-Pod：
  - 每个 Pod 都拥有一个独立 IP 地址
  - Pod 内所有容器共享一个网络命名空间

- 扁平网络：集群内所有 Pod 都在一个直接连通的扁平网络中，可通过 IP 直接访问
  - 所有容器之间无需 NAT 就可以直接互相访问
  - 所有 Node 和所有容器之间无需 NAT 就可以直接互相访问
  - 容器自己看到的 IP 跟其他容器看到的一样
  
- 内网分离：
  - Service cluster IP 实现 LB，尽可在集群内部访问
  - 外部请求需要通过 NodePort、LoadBalance 或者 Ingress 来访问

## 网络类型

### Pod-level

#### hostPort

hostPort 相当于`docker run -p 30890:80`，为容器在主机上做个 NAT 映射，不用创建 svc，因此端口只在容器运行的 vm 上监听。但是其缺点是无法负载多 pod。

```shell
kubectl apply -f 10_pod1-host-pod.yaml
curl localhost:30890 # Docker-Desktop doesn't work
```

#### hostNetwork

hostNetwork 相当于 `docker run --net=host`，与主机共享 network 网络栈，不用创建svc，因此端口只在容器运行的 vm 上监听。

```shell
kubectl apply -f 12_pod2-host-network.yaml
```

### Service-level

#### nodePort

由 kube-proxy 操控为所有节点统一配置 iptables 规则。因此，svc 上的 nodeport 会监听在所有的节点上。即使有 1 个 pod，访问任意节点的 nodeport 都可以访问到这个服务。

```shell
kubectl apply -f 20_service1-node-port.yaml
curl 127.0.0.1:30888 # Docker-Desktop works!
```

#### externalIPS(tmp)

通过 svc 来实现pod间的负载，但要求只监听某台指定 node 上，而非像 nodeport 那样监听所有节点。

```shell
kubectl apply -f 22_service2-external-ip.yaml
```

> 需要修改`22_service2-external-ip.yaml`，设置正确的节点IP

## Ingress Controller

- [Ingress Controller](30_ingress/README.md)
