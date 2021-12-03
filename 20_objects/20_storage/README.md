# Storage

## Etcd-based

### ConfigMap

We can consider ConfigMap as a PV/dir which contains a set of *variables* or files.  

- variables (key-value): if cm is mounted, key is displayed as file in the dir, value as content of the file
- file: if cm is mounted, file is displayed as file in the dir

#### CMD

- create
  - `kubectl apply -f cm1.yaml`: create from a YAML file
  - `kubectl apply -f cm1-pod-env.yaml`：create a pod with the cm
  - `kubectl exec cm1-pod-env -- env`: display the env variables
  - `kubectl create configmap cm2 --from-file=./configs`: create from a host dir 
  - `kubectl create configmap cm3 --from-file=./configs/db.conf --from-file=./configs/cache.conf`: create from a host file
  - `kubectl create configmap cm4 --from-literal=key1=value1`: create from a key-value
- apply: pass CM as file to ENV
  - `kubectl apply -f cm5-pod-env.yaml`
  - `kubectl logs cm5-pod-env`
- apply: pass CM as data to ENV
  - `kubectl create -f cm6-pod-env.yaml`
  - `kubectl logs cm6-pod-env`
- mount Config to pod as volume: key-->文件名，value-->文件的内容
  - `kubectl create -f cm7-pod-vol.yaml`
  - `kubectl exec cm7-pod-vol -- ls /etc/config`

### Secret

Secret是用来保存和传递密码、密钥、认证凭证这些敏感信息的对象。使用Secret的好处是可以避免把敏感信息明文写在配置文件里。在K8s集群中配置和使用服务不可避免的要用到各种敏感信息实现登录、认证等功能，例如访问AWS存储的用户名密码。为了避免将类似的敏感信息明文写在所有需要使用的配置文件中，可以将这些信息存入一个Secret对象，而在配置文件中通过Secret对象引用这些敏感信息。这种方式的好处包括：意图明确，避免重复，减少暴露机会。

创建secret时会用BASE64编码之后以同ConfigMap相同的方式存到Etcd，当mount到一个pod时会先解密在挂载

使用场景：docker-registry、generic、tls

#### 编码、解码

- `echo -n 'admin' | base64` --> YWRtaW4=
- `echo -n 'redhat' | base64` --> cmVkaGF0
- `echo 'YWRtaW4=' | base64 --decode` --> admin
- `echo 'cmVkaGF0' | base64 --decode` --> redhat

#### CMD

- `kubectl apply -f secret1.yaml`
- `kubectl get secret`
- `kubectl apply -f secret2.yaml`
- `kubectl apply -f secret2-pod-env.yaml`
- `kubectl apply -f secret3-pod-volume.yaml`
- `kubectl exec secret3-pod-volume -- ls /xxx`

## Volume-based

PV和PVC使得K8s集群具备了存储的逻辑抽象能力，使得在配置Pod的逻辑里可以忽略对实际后台存储技术的配置，而把这项配置的工作交给PV的配置者，即集群的管理者。存储的PV和PVC的这种关系，跟计算的Node和Pod的关系是非常类似的；PV和Node是资源的提供者，根据集群的基础设施变化而变化，由K8s集群管理员配置；而PVC和Pod是资源的使用者，根据业务服务的需求变化而变化，由K8s集群的使用者即服务的管理员来配置。

### Pod Volume
必须在定义pod的时候同时定义pod volume，其生命周期为pod的生命周期。

Volume is always hosted by each local node. 

#### emptyDir
Create a new empty dir for the volume
- `kubectl create -f vol1-emptydir.yaml`
- `kubectl exec vol1-emptydir -- ls /data`: manipulate on the volume

#### hostPath
Use an existing dir for the volume
- `kubectl create -f vol2-hostpath.yaml`
- `kubectl exec vol2-hostpath -- ls /data`: manipulate on the volume


### Persistent Volume
#### Persistent Volume (VP)
对底层共享存储的抽象。
Independent from pods, has the life-cycle as the whole k8s cluster.
PV is not hosted on a node, it belongs to the k8s cluster.

##### 访问模式
- (RWO) ReadWriteOnce – the volume can be mounted as read-write by a single node (单node的读写) 
- (ROM) ReadOnlyMany – the volume can be mounted read-only by many nodes (多node的只读) 
- (RWM) ReadWriteMany – the volume can be mounted as read-write by many nodes (多node的读写) 

##### 回收策略
- Retain 保留策略：允许人工处理保留的数据。（默认）
- Delete 删除策略：将删除pv和外部关联的存储资源，需要插件支持。
- Recycle 回收策略：将执行清除操作，之后可以被新的pvc使用，需要插件支持。

##### PV卷阶段状态
- Available – 资源尚未被claim使用
- Bound – 卷已经被绑定到claim了
- Released – claim被删除，卷处于释放状态，但未被集群回收。
- Failed – 卷自动回收失败

##### CMD
- `kubectl apply -f pv1.yaml`

#### PersistentVolumeClaim (VPC)
用户对于存储资源的申请。
PVC is used to create a PV which will be later declared and used in a pod.

- `kubectl apply -f pvc1.yaml`: create a PVC which will bound to the PV1
- `kubectl apply -f pvc1-pod.yaml`
- `kubuctl exec pvc1-pod -- ls /data`

#### Storage Class
- `kubectl create -f sc.yaml`: create a default storage class
- `kubectl create -f pvc-sc.yaml`: create a PVC
- `kubectl create -f pod-pvc-sc.yaml`: create a pod using the PVC
- `kubectl exec -it storage-pvc-sc -- /bin/sh`: access to the pod and test the storage

## Third-party Drivers

### Ceph

- [Ceph](ceph/README.md)




