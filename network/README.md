# Network
## Ingress
### Ingress Controller
Ingress Controller将基于Ingress规则将client的request直接转发到service对应的后端endpoint（即pod）上，这样会跳过kube-proxy的转发功能。
Ingres Controller以DaemonSet的形式创建，在每个node上启动以Pod hostPort的方式一个Nginx服务。

### Ingress策略
Ingress策略定义的path需要与后端真实Service的path一致，否则将会转发到一个不存在的path上。


