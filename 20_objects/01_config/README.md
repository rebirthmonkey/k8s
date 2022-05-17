# Config

## Context

通过 kubectl 连接 k8s 集群时，默认情况下 kubectl 会在 $HOME/.kube 目录下查找名为 config 的文件。

context = cluster + user

在将 cluster、用户和 context 定义在配置文件中之后，用户可以使用 kubectl config use-context 命令快速地在集群之间进行切换。针对每个集群都有对应的 kubeconfig 文件，文件中连接的 user、cluster 都与 contexts 对应。

### CMD

```shell
$ kubectl config view # 查看config配置信息
$ kubectl config get-contexts
$ kubectl config current-context
$ kubectl config use-context cluster2
```

### Lab

创建一个空目录，用于存放config-demo，即我们意图构造的**虚假的**配置文件

```shell
$ mkdir demo-config && cd demo-config
```

输入以下命令，则该目录下config-demo文件中的相关内容都会被修改。

> 如果该文件不存在则会被创建
> 也可以将`--kubeconfig=config-demo`中的`config-demo`替换成别的名称

- set

```shell
$ kubectl config --kubeconfig=config-demo set-cluster development --server=https://1.2.3.4 --certificate-authority=fake-ca-file
$ kubectl config --kubeconfig=config-demo set-cluster scratch --server=https://5.6.7.8 --insecure-skip-tls-verify
$ kubectl config --kubeconfig=config-demo set-credentials developer --client-certificate=fake-cert-file $ --client-key=fake-key-seefile
$ kubectl config --kubeconfig=config-demo set-credentials experimenter --username=exp --password=some-password
$ kubectl config --kubeconfig=config-demo set-context dev-frontend --cluster=development --namespace=frontend --user=developer
$ kubectl config --kubeconfig=config-demo set-context dev-storage --cluster=development --namespace=storage --user=developer
$ kubectl config --kubeconfig=config-demo set-context exp-scratch --cluster=scratch --namespace=default --user=experimenter
```

- use

```shell
kubectl config --kubeconfig=config-demo use-context dev-frontend
```

该命令的含义是：

- 读取`config-demo`
- `use-context`，使用一个context
- `dev-frontend` context名字是`dev-frontend`
