# Namespace

## 简介

Namespace 是一组对资源和对象的抽象集合，可以用来将系统内部的对象划分为不同的组。常见的 pod、deployment、service 等都必须属于某个 namespace，而 node、pv 等资源不属于任何 namespace。

在默认情况下，新的 k8s 集群上有三个 namespace：

- **default：**向集群中添加对象而不提拱 namespace，这样它会被放入默认的命名空间中，默认不需要输入 namespace的 名字。在创建替代的 namespace 之前，该 namespace 会充当用户新添加资源的主要目的地，无法删除。
- **kube-public：**kube-public namespace 的目的是让所有具有或不具有身份验证的用户都能全局可读。这对于公开 bootstrap 组件所需的集群信息非常有用。它主要是由 k8s 自己管理。
- **kube-system：**kube-system命名空间用于 k8s 管理的组件。一般规则是，避免向该 namespace 添加普通的工作负载。它一般由系统直接管理，因此具有相对宽松的策略。

### 资源控制

Namespace 还可以将策略应用到集群的具体部分，可以通过定义 ResourceQuota 对象来控制资源的使用，该对象在每个 namespace 的基础上设置了使用资源的限制。类似地，当在集群上使用支持网络策略的 CNI时，如 Calico 或 Canal ，可以将 NetworkPolicy 应用到 namespace，其中的规则定义了 pod 之间如何彼此通信。不同的 namespace 可以有不同的策略。

使用 namespace 最大的好处之一是能够利用 k8s 的 RBAC  访问控制。RBAC 允许在单个名称下开发角色，这样将权限或功能列表分组。ClusterRole 对象用于定义集群规模的使用模式，而角色对象类型（Role object  type）应用于具体的命名空间，从而提供更好的控制和粒度。在角色创建后，RoleBinding 可以将定义的功能授予单个 namespace 上下文中的具体具体用户或用户组。通过这种方式，namespace 可以使得集群操作者能够将相同的策略映射到组织好的资源集合。

### 使用模式

namespace 是一种非常灵活的特性，它不强制使用特定的模式。不过尽管如此，还是有许多在团队内常使用的模式。

- 将 namespace 映射到团队或项目上：在设置命名空间时有一个惯例是，为每个单独的项目或团队创建一个 namespace。通过给团队提供专门的 namespace，可以用 RBAC 策略委托某些功能来实现自动化。比如从 namespace 的 RoleBinding 对象中添加或删除成员就是对团队资源访问的一种简单方法。除此之外，给团队和项目设置资源配额也非常有用。有了这种方式，可以根据组织的业务需求和优先级合理地访问资源。
- 使用 namespace 对生命周期环境进行分区：namespace 非常适合在集群中划分开发、staging 以及生产环境。通常情况下，将生产工作负载部署到一个完全独立的集群中，来确保最大程度的隔离。不过对于较小的团队和项目来说，namespace 是一个可行的解决方案。在测试和发布对象时，可以把它们放到新环境中，同时保留其 namespace。这样可以避免因为环境中出现相似的对象而产生的混淆，并且减少认知开销。

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
