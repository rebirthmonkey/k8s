# kube-dns
## Installation


## Components
![kube-dns architecture](figures/kube-dns.png)

### kubedns
- watch the kube-apiserver to add new DNS entries

### dnsmasq
- cache the DNS entries and response for pod DNS lookup
- pod
  - each pod checks DNS through this component, k8s configures `/etc/resolv.conf` when launches a pod
  - name server: DNS server
  - search: automatically add domain name, k8s default domain is `SVC_ID.NAMESPACE_ID.svc.cluster.local`  
  - `ping` automatically add *search domain*
  - `nslookup` doesn't add *search domain*

### sidecar
-  healthz check kubedns and dnsmasq

### Volume: kube-dns-config
- [ConfigMap Yaml File](dns-configmap.yaml)


## TO-DO
- setup an external DNS
- config ConfigMap to use the external DNS server as an external server


## Ref
- [kubernetes之kubedns部署](http://blog.51cto.com/newfly/2059972)
- [Kubernetes技术分析之DNS](http://dockone.io/article/543)
- [kubernetes 简介：kube-dns 和服务发现](http://cizixs.com/2017/04/11/kubernetes-intro-kube-dns)
- [Configuring Private DNS Zones and Upstream Nameservers in Kubernetes](https://kubernetes.io/blog/2017/04/configuring-private-dns-zones-upstream-nameservers-kubernetes/)