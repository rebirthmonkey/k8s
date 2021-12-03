# 安装配置
## Installation

### Docker-for-Desktop

有时候k8s一直处于starting的状态，是因为很多k8s需要的进行无法pull下来，具体方法可以手动按照特定版本的Docker-for-Desktop，然后按照[教程](https://github.com/gotok8s/k8s-docker-desktop-for-mac)通过脚本手动下载所有镜像。

### Docker

#### Package Installation

If you have a Ubuntu, try next method

```shell
curl https://get.docker.com/ | sh
wget -qO- https://get.docker.com/ | sh
```

#### Ubuntu APT Installation

```shell
sudo apt-get remove docker docker-engine docker.io
sudo apt-get remove docker-compose
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
```


#### No-Root Configuration

```shell
sudo groupadd docker
sudo usermod -aG docker $USER
# logout and then login to take effect
```

#### Chinese Docker Repo Mirrors

(Skip)

```bash
sudo vi /etc/docker/daemon.json
```

Add following content to the file

```json
{
  "registry-mirrors": ["https://registry.docker-cn.com"]
}
```

Then

```bash
systemctl daemon-reload
systemctl restart docker
```


#### Test

```shell
docker --version
docker info
docker run hello-world
```

#### Troubleshooting

##### Failed to start Docker Application Container Engine

Cannot load hosts in configuration json file when starting docker daemon【1】

```shell
vim /lib/systemd/system/docker.service
ExecStart=/usr/bin/dockerd
# -H fd://
```

### kubectl

Reference: https://kubernetes.io/docs/tasks/tools/install-kubectl/

```shell
curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl
echo "source <(kubectl completion bash)" >> ~/.bashrc`: auto-completion in bashrc
```

Check Status

```shell
kubectl get componentstatuses
kubectl -n kube-system get pod
```

### Others

- [kubeadm](kubeadm/README.md)
  - `minikube start --memory 3072`: start minikube
  - `minikube dashboard`: check
- [minikube](minikube/README.md)
- [helm](../50_charts/README.md)


## Configuration
### Auto-completion
#### MacOS
More details can be find [here](https://www.e-learn.cn/content/qita/2054926).

```shell
brew install bash-completion

kubectl completion bash > $(brew -- prefix)/etc/bash_completion.d/kubectl

brew info bash-completion

[ -f /usr/local/etc/bash_completion ] && . /usr/local/etc/bash_completion # added in ~/.bash_profile

# restart the terminal
```

### Image Registry Mirrors

- `/etc/docker/daemon.json`：set default image register (no need to do)

  ```shell
  {
    "registry-mirrors": ["https://10.123.97.147"],  
    "max-concurrent-downloads": 6,
    "insecure-registries" : ["docker-registry.xxx.com"] 
  }
  ```

### Context
context in k8s is configuration setting of 1 cluster

```shell
kubectl config get-contexts # context is the config of a k8s cluster for kubectl
kubectl config set-context $CONTEXT_ID --user=admin-formation --cluster=cluster-demo # setup a context
kubectl config use-context $CONTEXT_ID # switch to another K8S context
```

## Ref

1. [Official documentation for installation](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
