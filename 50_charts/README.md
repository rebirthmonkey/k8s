# Helm
## Introduction
### Terminology
- chart：是Helm管理的安装包，里面包含需要部署的安装包资源
- release：是chart的部署实例，一个chart可以部署多个release，即这个chart可以被安装多次
- repository：chart的仓库，用于发布和存储chart

### chart包
每个chart包含下面两部分：
- Chart.yaml：描述本chart的基本信息，如名称版本等 
- values.yaml：chart配置的默认值
- templates：存放k8s manifest文件模板的目录，模板使用chart配置的值生成k8s manifest（yaml）文件
- charts：本chart需要依赖的其他chart

### Helm2 Architecture
- 客户端bin：通过gRPC连接到服务器端Tiller
- 服务器端Tiller：用来调用k8s api-server


## Installation
### Helm2
版本: v2.9.1
- `cd /data`
- `wget http://openstack.oa.com/tshift/helm-v2.9.1-linux-amd64.tar.gz`: download Helm client
- `docker pull docker-registry.tshift-test.oa.com/tiller:v2.9.1`: download Helm Tiller
- `yum install -y socat`
- `tar -zxvf helm-v2.9.1-linux-amd64.tar.gz`
- `mv linux-amd64/helm /usr/local/bin/helm`: install Helm client
- `helm init --tiller-image tiller:v2.9.1 --skip-refresh`

### Helm3 Docker-for-Desktop

```bash
curl -s https://get.helm.sh/helm-v3.1.0-darwin-amd64.tar.gz | tar xzv
sudo cp darwin-amd64/helm /usr/local/bin
rm -rf darwin-amd64
```

### Init & 测试

```bash
helm version
helm repo add stable https://mirror.azure.cn/kubernetes/charts/
helm repo add incubator https://mirror.azure.cn/kubernetes/charts-incubator/
helm repo update
helm install my-redis stable/redis
helm uninstall my-redis
```



- `docker pull nginx:1.15`
- `helm create hello-helm`
- `helm install ./hello-helm`
- `export POD_NAME=$(kubectl get pods --namespace default -l "app=hello-helm,release=fallacious-snail" -o jsonpath="{.items[0].metadata.name}")`
- `kubectl port-forward $POD_NAME 8080:80`
- `echo "Visit http://127.0.0.1:8080 to use your application"`


## Manipulation
### Repo

- `helm repo update`

### Release

- `helm create hello-svc`: create a Helm package
- `helm install --dry-run --debug ./`：验证模板和配置
- `helm install ./`：启动本chart的release
- `helm list`：list release
- `helm delete wishful-squid`

## Reference
- [是时候使用Helm了：Helm, Kubernetes的包管理工具](https://www.kubernetes.org.cn/3435.html)
- [简化Kubernetes应用部署工具-Helm简介](https://blog.csdn.net/M2l0ZgSsVc7r69eFdTj/article/details/78164002)