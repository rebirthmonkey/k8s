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

### Architecture
- 客户端bin：通过gRPC连接到服务器端Tiller
- 服务器端Tiller：用来调用k8s api-server


## Installation
- [installation](installation/README.md)


## Manipulation
- `helm init`：install Tiller
- `helm version`:

### Release
- `helm create hello-svc`: create a Helm package
- `helm install --dry-run --debug ./`：验证模板和配置
- `helm install ./`：启动本chart的release
- `helm list`：list release
- `helm delete wishful-squid`

### Repo
- `helm repo update`

## Reference
- [是时候使用Helm了：Helm, Kubernetes的包管理工具](https://www.kubernetes.org.cn/3435.html)
- [简化Kubernetes应用部署工具-Helm简介](https://blog.csdn.net/M2l0ZgSsVc7r69eFdTj/article/details/78164002)