# 手动部署kubeadm

仅用于理解组件之间的交互，但生产不推荐，因为无法维护、无法保证参数配置最佳，详见[参考文档](https://github.com/kelseyhightower/kubernetes-the-hard-way)。

## Reference

Here is the documentation for the installation:
[https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/)

## 安装准备

Kubeadm安装Kubernetes 1.13准备工作

- 基础环境介绍

```yaml
    系统：CentOS 7.6 64bit（Infrastructure server）
    内核：Linux 3.10.0-957.el7.x86_64  
    系统盘：100G
    网卡：仅主机  
    机器数量：3台
    CPU：2核
    内存：推荐4G内存，最少2G
    docker：docker-ce-18.06.1.ce-3.el7.x86_64
    注意：配置主机名、IP地址、网关、DNS均为静态获取
```

- hosts表

```text
    10.6.16.1   master01
    10.6.16.2   node01
    10.6.16.3   node02
```

- 软件包列表
  - CentOS-7-x86_64-DVD-1810.iso
  - container-selinux-2.68-1.el7.noarch.rpm  
  - docker-ce-18.06.1.ce-3.el7.x86_64.rpm
  - kubectl-1.13.0-0.x86_64.rpm
  - cri-tools-1.12.0-0.x86_64.rpm
  - kubelet-1.13.0-0.x86_64.rpm
  - kubeadm-1.13.0-0.x86_64.rpm
  - kubernetes-cni-0.6.0-0.x86_64.rpm
  - kube-images.tgz
  - calico.tgz

## 所有节点配置安装

1. 关闭firewalld：`systemctl disable firewalld.service`
2. 关闭SELinux：`sed -i 's/SELINUX=enforcing/SELINUX=disabled/' /etc/selinux/config`
3. 关闭swap
     - `swapoff -a`：临时关闭swap
     - 注释掉/etc/fstab下的swap一行：永久关闭swap
4. 配置本地yum源

    > 为什么要关闭swap: 当内存不足时，Linux会自动使用swap，将部分内存数据存放到磁盘中。而我们设想中，节点资源不足时，容器应该及时被迁移到资源充分的节点上，而不是勉强在内存不足的节点上运行

    > 为什么要关闭防火墙： 因为k8s使用`iptables`对IP规则进行转发修改，因此禁用其他的防火墙

    ```shell
    mkdir /etc/yum.repos.d/bak && mv /etc/yum.repos.d/*.repo /etc/yum.repos.d/bak/
    mount /xxx/CentOS-7-x86_64-DVD-1810.iso /mnt
    echo "mount /xxx/CentOS-7-x86_64-DVD-1810.iso /mnt" >> /etc/rc.local
    chmod u+x /etc/rc.local
    cat <<EOF > /etc/yum.repos.d/CentOS-Media.repo
    [c7-media]
    name=CentOS-$releasever - Media
    baseurl=file:///mnt
    gpgcheck=0
    enabled=1
    EOF
    ```

5. 安装docker

    ```shell
    cd docker-ce-18.06.1/
    yum -y install container-selinux-2.68-1.el7.noarch.rpm  docker-ce-18.06.1.ce-3.el7.x86_64.rpm
    docker info
    ```

6. 安装iptables

    ```shell
    yum -y install iptables-services.x86_64
    systemctl start iptables.service & systemctl enable iptables.service 
    iptables -F && iptables -t nat -F && iptables -t mangle -F && iptables -X
    iptables -P FORWARD ACCEPT
    service iptables save
    ```

7. 配置转发相关参数

    ```shell
    cat <<EOF >  /etc/sysctl.d/k8s.conf
    net.bridge.bridge-nf-call-ip6tables = 1
    net.bridge.bridge-nf-call-iptables = 1
    EOF
    sysctl --system
    systemctl restart docker.service
    ```

8. 安装kubelet、kubeadm、kubectl

    ```shell
    cd kube-1.13.0/
    yum -y install kubectl-1.13.0-0.x86_64.rpm \
    cri-tools-1.12.0-0.x86_64.rpm \
    kubelet-1.13.0-0.x86_64.rpm \
    kubeadm-1.13.0-0.x86_64.rpm \
    kubernetes-cni-0.6.0-0.x86_64.rpm
    systemctl start kubelet && systemctl enable kubelet
    ```

9. 配置kubelet的cgroups

    ```shell
    DOCKER_CGROUP=$(docker info | grep Cgroup | awk '{print $3}')
    echo $DOCKER_CGROUP
    cat >/etc/sysconfig/kubelet<<EOF
    KUBELET_EXTRA_ARGS=--cgroup-driver=$DOCKER_CGROUP
    EOF
    systemctl daemon-reload && systemctl enable kubelet && systemctl restart kubelet
    ```

## Master节点配置

1. master节点docker导入核心组件的images

    ```shell
    tar -xvf kube-images.tgz
    cd kube-images/
    for i in `ls`;do docker load < $i; done
    ```

2. 初始化master节点：注意修改apiserver IP地址（出现报错，请执行`kubeadm reset`命令）

    ```shell
    kubeadm init \
    --kubernetes-version=v1.13.0 \
    --pod-network-cidr=192.168.0.0/16 \
    --apiserver-advertise-address=10.6.18.11
    ```

3. 配置用户使用k8s集群
     - 普通用户管理Kubernetes集群

       ```shell
       mkdir -p $HOME/.kube
       sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
       sudo chown $(id -u):$(id -g) $HOME/.kube/config
       ```

     - root用户管理Kubernetes集群

        ```shell
            echo "export KUBECONFIG=/etc/kubernetes/admin.conf" >> /root/.bashrc
        ```

4. 配置kubernetes网络

    ```shell
    tar -xvf calico.tgz
    cd calico
    for i in `ls images`;do docker load < images/$i; done
    kubectl apply -f rbac-kdd.yaml
    kubectl apply -f calico.yaml
    ```

5. kubectl自动补全
     - 安装系统的bash-completion包：`yum install -y bash-completion`
     - 查看completion帮助：`kubectl completion -h
     - 若要将kubectl自动补全添加到当前shell：`source <(kubectl completion bash)`
     - 将kubectl自动补全添加到配置文件中，可以在以后的shell中自动加载它`echo "source <(kubectl completion bash)" >> ~/.bashrc`
     - 登出再登入

6. 检测Kubernetes集群是否正常

    ```shell
    kubectl get componentstatuses               //检查组件状态是否正常
    kubectl -n kube-system get pod              //查看核心组件是否运行正常（Running）
    ```

### 创建token、获取ca证书sha256编码hash值

1. 创建新的token`kubeadm token create`
2. 查看token`kubeadm token list`
3. 获取获取ca证书sha256编码hash值

```shell
openssl x509 -pubkey -in /etc/kubernetes/pki/ca.crt | openssl rsa -pubin -outform der 2>/dev/null | \
openssl dgst -sha256 -hex | sed 's/^.* //'
```

## node节点配置

1. 导入node节点kubernetes核心组件images

    ```shell
    tar -xvf kube-images.tgz
    cd kube-images
    docker load < kube-proxy-v1.13.0.tar
    docker load < pause-3.1.tar
    ```

2. 导入node节点calico组件的images

    ```shell
    tar -xvf calico.tgz
    for i in `ls calico/images`;do docker load < calico/images/$i; done
    ```

3. 导入node节点metrics组件的images

    ```shell
    cd metrics
    docker load < metrics.tar
    ```

4. 将Node节点添加到集群

    ```shell
    kubeadm join --token 83d49b.a1ai2c3rpqa89c4r 10.6.18.11:6443 --discovery-token-ca-cert-hash sha256:1e73f814eec04e3725573b42f8c177929934d01a00198c5dd8cce114f3b0f525
    ```
