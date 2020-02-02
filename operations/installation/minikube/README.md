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
- `minikube start --memory 3072`: start minikube
- `minikube dashbor`: check