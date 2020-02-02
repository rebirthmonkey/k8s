# kubeadm for Vagrant
## Vagrant VM Installation
- `vagrant up`

## Master Initialization
- `vagrant ssh master`
- `sudo kubeadm reset`
- `sudo swapoff -a`
- `sudo kubeadm init --pod-network-cidr=192.168.0.0/16 --apiserver-advertise-address=88.88.88.2`
- `mkdir -p $HOME/.kube`
- `sudo cp -f /etc/kubernetes/admin.conf $HOME/.kube/config`
- `sudo chown $(id -u):$(id -g) $HOME/.kube/config`

- set up a network driver: `kubectl apply -f http://docs.projectcalico.org/v2.4/getting-started/kubernetes/installation/hosted/kubeadm/1.6/calico.yaml`
- remove default DNS server: `kubectl delete deployment kube-dns --namespace=kube-system`
- dowload templates: `git clone https://git.opnfv.org/moon`
- install an update DNS server: `kubectl apply -f moon/moonv4/kubernetes/templates/kube-dns.yaml`
- make master work also as node: `kubectl taint nodes --all node-role.kubernetes.io/master-`
- enable access to Docker: `kubectl proxy&`
- test: `kubectl get pods --namespace=kube-system`

## Node Initialization
- node: `sudo kubeadm join --token fdaae4.96ec9aa698065a40 88.88.88.2:6443 --discovery-token-ca-cert-hash sha256:04270543e0398565877970b72da4026a93b31213467226e63d37d05aee000710`
- master: `kubectl get nodes`
