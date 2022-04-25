# minikube

minikube is a single-node (VM) cluster

## Installation

Here is the documentation for the installation:
[https://kubernetes.io/docs/tasks/tools/install-minikube/](https://kubernetes.io/docs/tasks/tools/install-minikube/)

Installation in China:
[https://my.oschina.net/u/228832/blog/3079150](https://kubernetes.io/docs/tasks/tools/install-minikube/)

The following part is for macOS

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
- `minikube start --memory 3072`: start minikube
- `minikube dashbor`: check
