# Network

Linux 容器能看见的“网络栈”是被隔离在它自己的 Network Namespace 中的网卡（Network Interface）、回环设备（Loopback Device）、路由表（Routing Table）和 iptables 规则。对于一个进程来说，这些要素实就构成了它发起和响应网络请求的基本环境。

## Intra-Host Network

### none

**none** 网络模式创建 Network namepace，但不配置任何网络功能，容器启动后可以自行为容器配置网络。容器启动时创建 Network Namepace，但不配置任何网络功能，以 --net=none参数启动容器。容器启动后可以为容器配置网络。

```bash
$ docker run --net=none ACCOUNT/focal:net ip addr show

1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
inet 127.0.0.1/8 scope host lo
valid_lft forever preferred_lft forever inet6 ::1/128 scope host
valid_lft forever preferred_lft forever
```

### Container Network

### container

如果指定 –net=container，**container**网络模式不创建 Network Namepace，而是加入另一个运行中的容器的 Network namespace。以 ``--net=container:<容器id>`` 参数启动容器。K8s 中 pod 的网络就使用了该模式，pod 中的容器都会加入 pod-init 容器创建的 Network namespace中。

```bash
$ docker run -it -d focal:net bash
a4f59725740788efc9ab3822d77e6d4714447c6854fcd8def30ec5f4415d5278
$ docker run --net=container:a4f597257407 -it -d focal:net bash 112d06adcaa2527d87ce9ed4b51ef1c3317d2ececbf19404d5402e8d710fa823 
$ docker inspect --format '{{.State.Pid}}' 112d06adcaa2
66156
$ docker inspect --format '{{.State.Pid}}' a4f597257407
12630
$ ls -l /proc/66156/ns/net
/proc/66156/ns/net -> net:[4026532355] 
$ ls -l /proc/65571/ns/net 
/proc/65571/ns/net -> net:[4026532355]
```

- `docker run -d -it --name=CT_ID ubuntu:focal`
- `docker run -d -it --network=container:CT_ID ubuntu:focal`: the containers share the same network stack

### Host

不创建 Network Namepace ，共享主机的Network Namespace，以 ``--net=host`` 参数启动容器。它会和宿主机上的其他普通进程一样，直接共享宿主机的网络栈。但是安全问题，容器可以操纵主机的网络配置。

```bash
$ docker run --net=host -it -d focal:net bash
b55213be4c805925ecc4dc1bd7934a01dde6f085313e395777c137b957d91a05
$ docker inspect --format '{{.State.Pid}}' b55213be4c80
22865
$ ls -l /proc/1/ns/net
/proc/1/ns/net -> net:[4026531957]
$ ls -l /proc/22865/ns/net 
/proc/22865/ns/net -> net:[4026531957]
```

- `docker run -it --network=host ubuntu:focal`: container and host share the same network stack
  - for the reason of performance
  - use the container to config the host network stack

### Bridge

**bridge**网络模式是 Docker 默认的网络模式，它创建新 Network Namepace 、配置 docker0 Linux bridge、创建 veth pair，并且创建 iptables NAT 规则。同一宿主机上的容器之间通过 docker0 网桥互访，容器访问外网通过 iptable NAT 功能，容器可以通过宿主机端口映射对外暴露服务。

<img src="figures/image-20200202153831519.png" alt="image-20200202153831519" style="zoom: 25%;" />

### overlay

Docker原生的跨主机通信模型，核心是Linux网桥与vxlan隧道，并且通过KV系统（consul、etcd）同步路由信息。

<img src="figures/image-20200123234145099.png" alt="image-20200123234145099" style="zoom: 25%;" />

- `docker network list`: list all the networks
- `docker network inspect NET_ID`: show detailed information
- `docker network create NET_ID`: create
  - `docker network create -d DRIVER NET_ID`: specify the network driver to use, by default we use the Bridge
- `docker network rm NET_ID`: remove
- `docker container run --name ct1 -it --rm --net=NET_ID ubuntu:focal`: launch a CT in a network
- `docker network connect NET_ID CT_ID`: connect a CT to a network, one CT can be connected to multiple networks
- `docker network disconnect NET_ID CT_ID`: disconnect

## Lab

### VM-VM Ping

- in the host：

  ```bash
  docker network create net1
  docker run --name ct1 -it -d --net=net1 focal:net
  docker run --name ct2 -it --net=net1 focal:net /bin/bash
  ```

> `focal:net`为之前章节中创建的包含ping工具的镜像

- in the container `ct2`:

  ```bash
  ping ct1
  ```
