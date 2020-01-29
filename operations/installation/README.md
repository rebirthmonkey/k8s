# Installation & Configuration
## kubectl
### Installation
- `curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl`
- or `curl -O https://storage.googleapis.com/kubernetes-release/release/v1.8.0/bin/linux/amd64/kubectl`
- `chmod +x ./kubectl`
- `sudo mv ./kubectl /usr/local/bin/kubectl`
- `echo "source <(kubectl completion bash)" >> ~/.bashrc`: auto-completion in bashrc

### Context
context in k8s is configuration setting of 1 cluster
- `kubectl config get-contexts`: context is the config of a k8s cluster for kubectl
- `kubectl config set-context $CONTEXT_ID --user=admin-formation --cluster=cluster-demo`: setup a context
- `kubectl config use-context $CONTEXT_ID`: switch to another K8S context


## minikube
minikube is a single-node (VM) cluster
### Installation
- `sudo apt-get update && sudo apt-get install -y curl virtualbox`
- `curl -Lo minikube https://storage.googleapis.com/minikube/releases/v0.24.1/minikube-linux-amd64`
- `chmod +x minikube`
- `sudo mv minikube /usr/local/bin/`
- `minikube start --memory 3072 --kubernetes-version v1.8.0`
- `minikube dashboard`: check

### Manipulation
- `minikube ip`: IP address of the minikube node
- `minikube ssh`: ssh to minikube
- `kubectl version`: check version
- `kubectl cluster-info`: check cluster info


## kubeadm
kubeadm is a production version.
- [kubeadm Installation](kubeadm/README.md)

