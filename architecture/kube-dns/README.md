# kube-dns

## Components
### kubedns
- watch the apiserver 

### dnsmasq
- cache the DNS entries

### sidecar
-  healthz check kubedns and dnsmasq

### Volume: kube-dns-config



