# NetworkPolicy

对某一部分pod进行流入（ingress）和流出（egress）的控制。运用的NetworkPolicy的pod默认拒绝任何ingress和egress流量，然后通过在NetworkPolicy中设置的白名单放行名单中的inngress和egress流量。

如果需要使用NetworkPolicy功能，CNI网络插件就必须是支持NetworkPolicy，支持的CNI网络插件都维护着一个NetworkPolicy Controller，通过控制循环的方式对NetworkPolicy对象的增删改查做出响应，在宿主机上完成iptables规则的配置工作。目前已经实现NetworkPolicy的CNI插件包括Calico、Weave和kube-router等，但Flannel不支持，但可以在Flannel网络安装Calico插件。

## 语法

### ingress

TODO

### egress

TODO

### 范围

- ipBlock
- namespaceSelector
- podSelector

TODO
