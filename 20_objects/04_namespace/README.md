# Namespace
Namespace 是一组对资源和对象的抽象集合，可以用来将系统内部的对象划分为不同的组。常见的 pod、deployment、service 等都必须属于某个 namespace，而 node、pv 等资源不属于任何 namespace。

集群自身的核心服务一般运行在 kube-system 这个 namespace 中。刚创建集群时候存在一个 default 默认namespace，默认不需要输入 namespace的 名字。

### CMD
- list
    - `kubectl get namespaces`
- select
    - `kubectl -n kube-system get pods`: execute CMD within 1 namespace
- create
    - `kubectl create namespaces test`
    - `kubectl apply -f namespace.yaml` or `kubectl create -f namespace.yaml`
- delete
    - `kubeclt delete namespaces test`
    - `kubectl delete -f namespace.yaml`


## Monitor
- `kubectl top node`
- `kubectl -n kube-system top pod`


## Log
- `kubectl logs RESOURCE_ID`: logs
- `kubectl get event`