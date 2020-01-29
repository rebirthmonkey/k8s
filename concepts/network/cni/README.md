# CNI

## 简介

CNI的设计思想是：ks8在启动Pod Infra容器之后，就可以直接调用CNI网络插件，为这个Infra容器的Network Namespace配置符合预期的网络栈。

如果要实现一个k8s的CNI方案，例如Flannel，其实需要做两部分工作：

- 节点配置（CNI方案）：flanneld进程里的主要逻辑，如创建和配置flannel.1设备、配置宿主机路由、配置ARP和FDB表里的信息等等。
- Pod Infra配置（CNI插件）：配置Infra容器里面的网络栈，并把它连到CNI网桥上。安装时会把对应CNI插件的可执行文件放在 /opt/cni/bin/ 目录下。

## CNI方案：节点配置

在宿主机上安装网络方案（flanneld），flanneld启动后会在每台宿主机上生成它对应的CNI配置文件，从而告诉k8s这个集群要使用 Flannel 作为容器网络方案。k8s处理容器网络相关的逻辑并不在kubelet，而是会在具体的 CRI（Docker是dockershim）。所以dockershim会在 /etc/cni/net.d下加载CNI配置文件。CNI 允许在一个CNI 配置文件里，通过plugins字段定义多个插件进行协作。如Flannel就指定了 flannel 和 portmap 这两个插件。这时候，dockershim 会把这个 CNI 配置文件加载起来，并且把列表里的第一个插件、也就是 flannel 插件，设置为默认插件。而在后面的执行过程中，flannel 和 portmap 插件会按照定义顺序被调用，从而依次完成“配置容器网络”和“配置端口映射”这两步操作。

## CNI插件：Pod Infra配置

当kubelet需要创建 Pod 的时候，它会先创建pod的Infra容器。dockershim 就会先调用 Docker API 创建并启动 Infra 容器，紧接着执行一个叫作 SetUpPod 的方法为 CNI 插件准备参数，然后调用 CNI 插件为 Infra 容器配置网络。这里要调用的 CNI 插件，就是 /opt/cni/bin/flannel。调用它所需要的参数分为两部分：

- 第一部分，是由 dockershim 设置的一组 CNI 环境变量，其中最重要的环境变量参数叫作：CNI_COMMAND。它的取值只有两种：ADD 和 DEL。ADD就是把容器添加到 CNI 网络里，而DEL是把容器从 CNI 网络里移除掉。而对于网桥类型的 CNI 插件来说，这两个操作意味着把容器以 Veth Pair 的方式“插”到 CNI 网桥上，或者从网桥上“拔”掉。
- 第二部分，是 dockershim 从 CNI 配置文件里加载到的、默认插件的配置信息。这个配置信息在 CNI 中被叫作 Network Configuration。dockershim 会把 Network Configuration 以 JSON 数据的格式，通过标准输入（stdin）的方式传递给 Flannel CNI 插件。

CNI 配置文件（ /etc/cni/net.d/10-flannel.conflist）里有这么一个字段叫作 delegate，意思是本CNI会调用 Delegate 指定的某种 CNI 内置插件来完成。对于Flannel，它会调用CNI bridge插件，dockershim 对 Flannel CNI 插件的调用，其实就是走了个过场，具体时间是执行 /opt/cni/bin/bridge 二进制文件。

最后，CNI 插件会把容器的 IP 地址等信息返回给 dockershim，然后被 kubelet 添加到 Pod 的 Status 字段。至此，CNI 插件的 ADD 方法就宣告结束了。







