# Storage

## Pod Volume
必须在定义pod的时候同时定义pod volume，其生命周期为pod的生命周期。

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

#### 访问模式
- (RWO) ReadWriteOnce – the volume can be mounted as read-write by a single node (单node的读写) 
- (ROM) ReadOnlyMany – the volume can be mounted read-only by many nodes (多node的只读) 
- (RWM) ReadWriteMany – the volume can be mounted as read-write by many nodes (多node的读写) 

#### 回收策略
- Retain 保留策略：允许人工处理保留的数据。（默认）
- Delete 删除策略：将删除pv和外部关联的存储资源，需要插件支持。
- Recycle 回收策略：将执行清除操作，之后可以被新的pvc使用，需要插件支持。

#### PV卷阶段状态
- Available – 资源尚未被claim使用
- Bound – 卷已经被绑定到claim了
- Released – claim被删除，卷处于释放状态，但未被集群回收。
- Failed – 卷自动回收失败

#### CMD
- `kubectl apply -f pv.yaml`

### PersistentVolumeClaim (VPC)
用户对于存储资源的申请。
PVC is used to create a PV which will be later declared and used in a pod.
- `kubectl apply -f pvc.yaml`: create a PVC
- `kubectl apply -f pod-pvc.yaml`

### Storage Class
- `kubectl create -f sc.yaml`: create a default storage class
- `kubectl create -f pvc-sc.yaml`: create a PVC
- `kubectl create -f pod-pvc-sc.yaml`: create a pod using the PVC
- `kubectl exec -it storage-pvc-sc -- /bin/sh`: access to the pod and test the storage


## ConfigMap
We can consider ConfigMap as a PV/dir which contains a set of *variables* or files.  
- variables (key-value): if cm is mounted, key is displayed as file in the dir, value as content of the file
- file: if cm is mounted, file is displayed as fil in the dir

### CMD
- create
  - `kubectl create -f cm.yaml`: create from a YAML file
  - `kubectl create configmap cm1 --from-file=./configs`: create from a host dir 
  - `kubectl create configmap cm2 --from-file=./configs/db.conf --from-file=./configs/cache.conf`: create from a host file
  - `kubectl create configmap cm3 --from-literal=key1=value1`: create from a key-value
- apply: pass CM as file to ENV
  - `kubectl create -f pod-cm-env1.yaml`
  - `kubectl logs test-container`
- apply: pass CM as data to ENV
  - `kubectl create -f pod-cm-env2.yaml`
  - `kubectl logs storage-cm-env`
- mount Config to pod as volume: key-->文件名，value-->文件的内容
  - `kubectl create -f pod-cm-vol.yaml`
  - `kubectl exec -it storage-cm-env -- /bin/bash`


## Secret
创建时会用BASE64编码之后以同ConfigMap相同的方式存到Etcd，当mount到一个pod时会先解密在挂载

### 使用场景
- docker-registry
- generic
- tls

### 编码、解码
- `echo -n 'admin' | base64` --> YWRtaW4=
- `echo -n 'redhat' | base64` --> cmVkaGF0
- `echo 'YWRtaW4=' | base64 --decode` --> admin
- `echo 'cmVkaGF0' | base64 --decode` --> redhat

### CMD
- `kubectl create -f secret.yaml`
- `kubectl get secret`
- `kubectl create -f pod-secret-env.yaml`
- `kubectl create -f pod-secret-volume.yaml`

## Ceph
- [Ceph](ceph/README.md)




