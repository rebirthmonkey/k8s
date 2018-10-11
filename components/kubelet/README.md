# kubelet
处理master下发给本节点（node）的任务，管理本节点pod及其中的container。
- 在`API Server`上注册本node信息
- 通过`API Server`监听所有针对pod的操作，并做相关如创建、删除CT等的操作
- 通过cAdvisor监控container和node资源，并定期向master汇报资源使用情况
