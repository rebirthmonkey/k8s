# kube-scheduler
根据待调度pod列表、可用node列表、以及调度算法/策略，将待调度pod绑定到某个合适的node上，并将绑定信息写入etcd。