# Installation & Configuration
## Installation
- [kubeadm](kubeadm/README.md)
- [minikube](minikube/README.md)


## Configuration
### Auto-completion
#### MacOS
More details can be find [here](https://www.e-learn.cn/content/qita/2054926).
- `brew install bash-completion`
- `kubectl completion bash > $(brew --prefix)/etc/bash_completion.d/kubectl`
- `brew info bash-completion`
- `[ -f /usr/local/etc/bash_completion ] && . /usr/local/etc/bash_completion`: added in `~/.bash_profile`
- restart the terminal

## Manipulation
### kubectl Installation

    curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
    curl -O https://storage.googleapis.com/kubernetes-release/release/v1.8.0/bin/linux/amd64/kubectl
    chmod +x ./kubectl
    sudo mv ./kubectl /usr/local/bin/kubectl
    echo "source <(kubectl completion bash)" >> ~/.bashrc`: auto-completion in bashrc

### Check Status
- `kubectl get componentstatuses`
- `kubectl -n kube-system get pod`

### Context
context in k8s is configuration setting of 1 cluster
- `kubectl config get-contexts`: context is the config of a k8s cluster for kubectl
- `kubectl config set-context $CONTEXT_ID --user=admin-formation --cluster=cluster-demo`: setup a context
- `kubectl config use-context $CONTEXT_ID`: switch to another K8S context
