# Namespace

Namespace 是一组对资源和对象的抽象集合，可以用来将系统内部的对象划分为不同的组。常见的 pod、deployment、service 等都必须属于某个 namespace，而 node、pv 等资源不属于任何 namespace。

集群自身的核心服务一般运行在 kube-system 这个 namespace 中。刚创建集群时候存在一个 default 默认namespace，默认不需要输入 namespace的 名字。

## CMD

- list
    - `kubectl get namespaces`
- select
    - `kubectl -n kube-system get pods`: execute CMD within 1 namespace
- create
    - `kubectl create namespace test`
    - `kubectl apply -f namespace.yaml` or `kubectl create -f namespace.yaml`
- delete
    - `kubeclt delete namespace test`
    - `kubectl delete -f namespace.yaml`

## Monitor

和`top` 命令一样，kubectl可以监控节点的状态

- `kubectl top node`
- `kubectl -n kube-system top pod` 添加`-n`参数可以限定作用域

> 可能需要安装metrics-server
>
> ```shell
> wget https://github.com/kubernetes-sigs/metrics-server/releases/download/v0.3.6/components.yaml
> kubectl apply -f components.yaml

> 如果遇到metrics-server容器Running而无法Ready，容器日志中出现X509错误，则需要启用serverTLSBootstrap. 参考[官方文档](https://kubernetes.io/zh/docs/reference/command-line-tools-reference/kubelet-tls-bootstrapping/)

> 也可以在`components.yaml`文件下的`template.containers.args`下添加`--kubelet-insecure-tls`参数忽略证书错误，然后再次运行`kubectl apply -f components.yaml`

## Log

使用`kubectl logs`可以查看某一个resource的log

- `kubectl logs RESOURCE_ID`: logs
- `kubectl -n space logs RESOURCE_ID`: logs查看space命名空间下的RESOURCE_ID的log
- `kubectl get event`

> `RESOURCE_ID`需要替换成resource的ID，注意不同namespace下的RESOURCE_ID是不同的
> `kubectl get all`可以获取命名空间下所有resource，默认是default命名空间下
