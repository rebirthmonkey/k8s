# k8s Core Principles
## kube-apiserver
- `curl 127.0.0.1:8080/api`
- `curl 127.0.0.1:8080/api/v1`
- `curl 127.0.0.1:8080/api/v1/pods`

### K8S Proxy API
kube-apiserver把收到的REST request转发到某个node的kubelet的REST端口上。
通过k8s proxy API获得的数据来自node而非etcd。


## kube-controller-manager
- Replication Controller：RC所关联的pod副本数保持预设值，pod的RestartPolicy=Always
- Node Controller：kubelet通过API server注册自身节点信息
- ResourceQuota Controller：确保指定资源对象在任何时候都不会超量占用系统物力资源（需要Admission Control配合使用）
- Endpoint Controller：生成和维护所有endpoint对象
- Service Controller：监听、维护service的变化
- Namespace Controller
- ServiceAccount Controller
- Token Controller


## kube-scheduler
根据待调度pod列表、可用node列表、以及调度算法/策略，将待调度pod绑定到某个合适的node上，并将绑定信息写入etcd。


## kubelet
处理master下发的本node任务，管理本节点pod及其中的container。
每个kubelet会在API Server上注册node自身信息，定期向master汇报资源使用情况，并通过cAdvisor监控container和节点资源。


## kube-proxy
- 通过监听kube-apiserver获得service、endpoint变化
- 为每个service在每个node上建立一个SocketServer、在本node上监听一个临时端口：确保本host上的任何pod能访问该Service
- service的本地SocketServer会通过内部LB调用某个node的SocketServer
- LB保存了Service到Endpoint列表（SocketServer的临时端口）：确保了Service的clusterIP的request会被寄到任何一个node的pod上


## Security
### Authentication
- CA证书
- HTTP Token
- HTTP Base：Header Authorization = UserName:Password

### Authorization
API server收到一个request后，会根据其中数据创建access policy object，然后将这个object与access policy逐条匹配，如果有至少一条匹配，则鉴权通过。

#### WebHook

#### ABAC

#### RBAC
- Role：一个NS中一组权限的集合
- ClusterRole：整个k8s集群的一组权限的集合
- RoleBinding：把一个role绑定到一个user/group/serviceAccount，roleBinding也可使用clusterRole，把一个clusterRole运用在一个NS内。
- ClusterRoleBinding：把一个clusterRole绑定到一个user


### Admission Control

### ServiceAccount


