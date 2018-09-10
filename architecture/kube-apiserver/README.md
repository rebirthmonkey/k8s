# kube-apiserver
## URL
- `curl 127.0.0.1:8080/api`
- `curl 127.0.0.1:8080/api/v1`
- `curl 127.0.0.1:8080/api/v1/pods`

## K8S Proxy API
kube-apiserver把收到的REST request转发到某个node的kubelet的REST端口上。
通过k8s proxy API获得的数据来自node而非etcd。