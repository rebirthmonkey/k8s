# Network
## Intra-Host Network
### None

容器启动时创建Network Namepace，但不配置任何网络功能，以--net=none参数启动容器。容器启动后可以为容器配置网络。

```bash
$ docker run --net=none ACCOUNT/xenial:net ip addr show

1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
inet 127.0.0.1/8 scope host lo
valid_lft forever preferred_lft forever inet6 ::1/128 scope host
valid_lft forever preferred_lft forever
```



### Container Network

不创建Network Namepace，加入另一个运行中的容器的Network Namespace，以--net=container:<容器id>参数启动容器。k8s中的Pod就是基于container network建立的。

```bash
$ docker run -it -d xenial:net bash
a4f59725740788efc9ab3822d77e6d4714447c6854fcd8def30ec5f4415d5278
$ docker run --net=container:a4f597257407 -it -d xenial:net bash 112d06adcaa2527d87ce9ed4b51ef1c3317d2ececbf19404d5402e8d710fa823 
$ docker inspect --format '{{.State.Pid}}' 112d06adcaa2
66156
$ docker inspect --format '{{.State.Pid}}' a4f597257407
12630
$ ls -l /proc/66156/ns/net
/proc/66156/ns/net -> net:[4026532355] 
$ ls -l /proc/65571/ns/net 
/proc/65571/ns/net -> net:[4026532355]
```

- `docker run -d -it --name=CT_ID ubuntu:xenial`
- `docker run -d -it --network=container:CT_ID ubuntu:xenial`: the containers share the same network stack

### Host

不创建Network Namepace，共享主机的Network Namespace，以--net=host参数启动容器。但是安全问题，容器可以操纵主机的网络配置。

```bash
$ docker run --net=host -it -d xenial:net bash
b55213be4c805925ecc4dc1bd7934a01dde6f085313e395777c137b957d91a05
$ docker inspect --format '{{.State.Pid}}' b55213be4c80
22865
$ ls -l /proc/1/ns/net
/proc/1/ns/net -> net:[4026531957]
$ ls -l /proc/22865/ns/net 
/proc/22865/ns/net -> net:[4026531957]
```

- `docker run -it --network=host ubuntu:xenial`: container and host share the same network stack
  - for the reason of performance 
  - use the container to config the host network stack

### Bridge

Docker设计的NAT网络模型，创建新Network Namepace，配置docker0网桥，创建、配置对应的veth pair，依赖iptables规则，以--net=bridge参数启动容器。

容器之间通过docker0网桥实现互访，容器通过iptable NAT功能访问外网，同时容器通过宿主机端口映射对外暴露服务。

![image-20200202153831519](figures/image-20200202153831519.png)

- `docker network list`: list all the networks
- `docker network inspect NET_ID`: show detailed information
- `docker network create NET_ID`: create
  - `docker network create -d DRIVER NET_ID`: specify the network driver to use, by default we use the Bridge
- `docker network rm NET_ID`: remove
- `docker container run --name ct1 -it --rm --net=NET_ID ubuntu:xenial`: launch a CT in a network
- `docker network connect NET_ID CT_ID`: connect a CT to a network, one CT can be connected to multiple networks
- `docker network disconnect NET_ID CT_ID`: disconnect


## Lab
### VM-VM Ping
- in the host：
```bash
docker network create net1
docker run --name ct1 -it -d --net=net1 xenial:net
docker run --name ct2 -it --net=net1 xenial:net /bin/bash
```
- in the container `ct2`: 
```bash
ping ct1
```
