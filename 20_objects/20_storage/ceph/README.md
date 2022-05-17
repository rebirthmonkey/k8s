# Ceph

## Pre-requisite

- the Ceph client version should be higher than 12.2.2

## Secret

- `echo keyring | base64`: to secret.yaml-> key
- `kubectl create -f secret-luminous-admin.yaml`

## Ceph RBD

- `cp cepf.conf /etc/ceph`
- `cp ceph.client.admin.keyring /etc/ceph`
- `rbd create k8s/pv -s 1024`

### Pod with volume

- `cd ceph-rbd/luminous`
- `kubectl create -f rbd-pod-volume.yaml`
- `kubectl exec rbd-volume -- df -h| grep rbd`
- `kubectl exec rbd-volume -- cp /etc/hosts /mnt/rbd/`
- `kubectl exec rbd-volume -- cat /mnt/rbd/hosts`
- `kubectl delete -f rbd-pod-volume.yaml`
- `kubectl create -f rbd-pod-volume.yaml`
- `kubectl exec rbd-volume -- cat /mnt/rbd/hosts`: check the data
- `kubectl delete -f rbd-pod-volume.yaml`: cleanup

### PV/PVC

- `kubectl create -f rbd-pv.yaml`
- `kubectl create -f rbd-pvc.yaml`
- `kubectl create -f rbd-pod-pv.yaml`
- `kubectl exec rbd-pv -- cat /mnt/rbd/hosts`: check the data
- `kubectl delete -f rbd-pod-pv.yaml`
- `kubectl delete -f rbd-pvc.yaml`
- `kubectl delete -f rbd-pv.yaml`

### Storage Class

- `kubectl create -f rbd-sc.yaml`: install the Ceph-RBD storage class
- `kubectl get sc`
- `kubectl create -f rbd-pvc-sc.yaml`
- `kubectl create -f rbd-pod-sc.yaml`
- `kubectl exec -it rbd-sc -- /bin/sh`
- `kubectl delete -f rbd-pod-sc.yaml`
- `kubectl delete -f rbd-pvc-sc.yaml`

## CephFS

### FS Mount

- `mkdir /mnt/cephfs-root`
- `ceph-fuse -r / /mnt/cephfs-root/`: mount
- `touch /mnt/cephfs-root/xxx`
- `umount /mnt/cephfs-root`: umount

### Secret

- `cd cephfs/luminous`
- `kubectl create -f secret-luminous-admin.yaml`

### Pod with Volume

- `kubectl create -f cephfs-pod-volume.yaml`
- `kubectl exec -it cephfs-volume -- ls /mnt/cephfs`
- `kubectl delete -f cephfs-pod-volume.yaml`: cleanup

### PV/PVC

- `kubectl create -f cephfs-pv.yaml`
- `kubectl create -f cephfs-pvc.yaml`
- `kubectl create -f cephfs-pod-pv.yaml`
- `kubectl exec -it cephfs-pv -- ls /mnt/cephfs`

### Storage Class

- Install CephFS storage class controller with role: in the namespace *cephfs*
  - `cd cephfs/luminous/cephfs-sc-provisioner`
  - `kubectl create -f namespace.yaml`
  - `kubectl create -f serviceaccount.yaml`
  - `kubectl create -f clusterrole.yaml`
  - `kubectl create -f clusterrolebinding.yaml`
  - `kubectl create -f role.yaml`
  - `kubectl create -f rolebinding.yaml`
  - `kubectl create -f deployment.yaml`: the provisoner is hard-coded in the namespace *cephfs*
- `kubectl -n cephfs create -f secret-luminous-admin.yaml`
- `kubectl -n cephfs create -f cephfs-sc.yaml`
- `kubectl -n cephfs create -f cephfs-pvc-sc.yaml`
- `kubectl -n cephfs create -f cephfs-pod-sc.yaml`
- `kubectl -n cephfs exec -it cephfs-sc -- /bin/sh`

## Doc

- [K8S RBD](https://ieevee.com/tech/2018/05/16/k8s-rbd.html)
- [K8S CephFS](https://ieevee.com/tech/2018/05/17/k8s-cephfs.html)
