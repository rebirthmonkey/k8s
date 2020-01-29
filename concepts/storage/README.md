# Storage
## 基础
- [存储基础](basics.md)

## Volume (Pod-level)
Attached to a pod and has the same life-cycle as the pod, deleted when the pod is destroyed. 
Volume is always hosted by each local node. 

### emptyDir
Create a new empty dir for the volume
- `kubectl create -f pod-vol-emptydir.yaml`
- `kubectl exec -it storage-vol-emptydir -- /bin/bash`: manipulate on the volume

### hostPath
Use an existing dir for the volume
- `kubectl create -f pod-vol-hostpath.yaml`
- `kubectl exec -it storage-vol-hostpath -- /bin/bash`: manipulate on the volume


## Persistent Volume
### Persistent Volume (VP)
对底层共享存储的抽象。
Independent from pods, has the life-cycle as the whole k8s cluster.
PV is not hosted on a node, it belongs to the k8s cluster. 

### PersistentVolumeClaim (VPC)
用户对于存储资源的申请。
PVC is used to create a PV which will be later declared and used in a pod.
- `kubectl apply -f pvc1.yaml`: create a PVC

### Storage Class
- `kubectl create -f sc.yaml`: create a default storage class
- `kubectl create -f pvc-sc.yaml`: create a PVC
- `kubectl create -f pod-pvc-sc.yaml`: create a pod using the PVC
- `kubectl exec -it storage-pvc-sc -- /bin/sh`: access to the pod and test the storage


## ConfigMap
We can consider ConfigMap as a PV/dir which contains a set of *variables* or files.  
- variables (key-value): if cm is mounted, key is displayed as file in the dir, value as content of the file
- file: if cm is mounted, file is displayed as fil in the dir

### Creation
- `kubectl create -f cm.yaml`: create from a YAML file
- `kubectl create configmap cm1 --from-file=./configs`: create from a host dir 
- `kubectl create configmap cm2 --from-file=./configs/db.conf --from-file=./configs/cache.conf`: create from a host file
- `kubectl create configmap cm3 --from-literal=key1=value1`: create from a key-value

### Usage
Pass Config to pod as env
- `kubectl create -f pod-cm-env.yaml`
- `kubectl logs storage-cm-env`

Mount Config to pod as volume
- `kubectl create -f pod-cm-vol.yaml`
- `kubectl exec -it storage-cm-env -- /bin/bash`


## Secret
Secret用BASE64编码来保持敏感信息，只有当敏感信息被挂在到pod/CT中之后，才会解码敏感信息。

- `kubectl create -f secret.yaml`
- `kubectl get secret`


## Ceph
- [Ceph](ceph/README.md)
