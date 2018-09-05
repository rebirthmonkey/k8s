# Ceph
## Secret
- `echo keyring | base64`: to secret.yaml-> key
- `kubectl create -f secret-luminous-admin.yaml`

## Ceph RBD
- `rbd create k8s/pv -s 1024`
- `kubectl create -f secret-hammer-admin.yaml`

### rbd with volume
- `cd ceph-rbd/hammer`
- `kubectl create -f rbd-pod-volume.yaml`
- `kubectl exec rbd-volume -- df -h| grep rbd`
- `kubectl exec rbd-volume -- cp /etc/hosts /mnt/rbd/`
- `kubectl exec rbd-volume -- cat /mnt/rbd/hosts`
- `kubectl delete -f rbd-pod-volume.yaml`
- `kubectl create -f rbd-pod-volume.yaml`
- `kubectl exec rbd-volume -- cat /mnt/rbd/hosts`

### rbd with PV/PVC
- `kubectl create -f rbd-pv.yaml`
- `kubectl create -f rbd-pvc.yaml`
- `kubectl create -f rbd-pod-pv.yaml`
- `kubectl exec rbd-pv -- cat /mnt/rbd-pv/hosts`

### rbd with storage class
- `kubectl create -f rbd-sc.yaml`
- `kubectl get sc`
- `kubectl create -f rbd-pod-sc.yaml`


## CephFS
### Mount
- `mkdir /mnt/cephfs-root`
- `ceph-fuse -r / /mnt/cephfs-root/`: mount
- `touch /mnt/cephfs-root/xxx`
- `umount /mnt/cephfs-root`: umount

### Pod with Volume
- ???`kubectl create -f luminous/cephfs-pod-volume.yaml`: doesn't work

### PV/PVC
- `kubectl create -f luminous/cephfs-pv.yaml`
- `kubectl create -f luminous/cephfs-pvc.yaml`
- `kubectl create -f luminous/cephfs-pod.yaml`
- `kubectl exec -it cephfs -- cat /mnt/xxx/aaa`

### Storage Class
- doesn't work
