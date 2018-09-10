# Security
## Authentication
- CA证书
- HTTP Token
- HTTP Base：Header Authorization = UserName:Password


## Authorization
API server收到一个request后，会根据其中数据创建access policy object，然后将这个object与access policy逐条匹配，如果有至少一条匹配，则鉴权通过。


### WebHook


### ABAC


### RBAC
- Role：一个NS中一组权限的集合
- ClusterRole：整个k8s集群的一组权限的集合
- RoleBinding：把一个role绑定到一个user/group/serviceAccount，roleBinding也可使用clusterRole，把一个clusterRole运用在一个NS内。
- ClusterRoleBinding：把一个clusterRole绑定到一个user


## Admission Control


## ServiceAccount
