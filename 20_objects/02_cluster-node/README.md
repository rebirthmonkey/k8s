# Cluster & Node
## Cluster
### Terminology
- cluster: 1 or 3 master + n nodes
- master: a VM or a physical machine which coordinates the cluster
- node/worker: a VM or a physical machine which serves as a worker that runs applications
- namespace: virtual cluster for resource isolation

### Port
- pod port
  - containerPort: Docker image/container's exposed port
- service port
  - targetPort: *pod's containerPort*
  - port: service's port, clusterIP's port. If not specified, use the same as targetPort 
  - nodePort: node's exposed port for the service


## Node

Node 可以是物理机也可以是 VM，每个 node 上至少运行 kubelet 和 container runtime。默认情况下，kubelet 在启动时会自动向 k8s master 注册自己。

```bash
kubectl get nodes
kubectl describe nodes NODE_ID
```

Node包括以下信息：

- 地址：hostname、外网地址、内网地址
- Condition：OutOfDisk、Ready、MemoryPressure、DiskPressure
- Capacity：node上可用的资源，包括CPU、内存、Pod总数
- System Info：内核版本、容器引擎版本、OS类型等
- Allocable（可分配资源）：node上可用的资源，包括CPU、内存、Pod总数


### CMD

- `kubectl cluster-info`
- `kubectl get nodes`
  - `kubectl get nodes -o yaml`: -o output format
- `kubectl describe node NODE_NAME`: detail about a node

## Taint & Toleration

- taint：只有key=value的pod才会被调度到该node上，其他的pod一律不能被调度

  - NoSchedule：仅影响调度过程，对现存的Pod对象不产生影响；但容忍的pod同时也能够被分配到集群中的其它节点
  - NoExecute：既影响调度过程，也影响现在的Pod对象；不容忍的Pod对象将被驱逐
  - PreferNoSchedule：NoSchedule的柔性版本，最好别调度过来，实在没地方运行调过来也行
- toleration：针对taint，用于让pod被调度到之前taint key=value的node上

```yaml
  tolerations:
  - key: node-role.kubernetes.io/master
    effect: NoSchedule # taint 可以 key、effect 而没有 value
```

### CMD

```bash
kubectl taint node NODE_NAME taint1=test1:NoSchedule
kubectl taint node docker-desktop node-role.kubernetes.io/master=:NoSchedule # 可以 key、effect 而没有 value
kubectl describe nodes | grep Taints
kubectl taint node NODE_NAME taint1-
kubectl taint node docker-desktop node-role.kubernetes.io/master- # untaint
kubectl apply -f 20_taint-pod.yaml
```

## Cordon & Drain

设置某个节点为维护模式，不让其他 pod 调度上来

```bash
kubectl cordon NODE_NAME
kubectl get nodes
kubectl drain NODE_ID --ignore-daemonsets # 平滑迁移pod
kubectl uncordon NODE_ID # 取消节点的维护模式
```

