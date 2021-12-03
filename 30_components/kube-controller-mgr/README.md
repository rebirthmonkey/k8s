# kube-controller-manager

- Replication Controller：RC所关联的pod副本数保持预设值，pod的RestartPolicy=Always
- Node Controller：kubelet通过API server注册自身节点信息
- ResourceQuota Controller：确保指定资源对象在任何时候都不会超量占用系统物力资源（需要Admission Control配合使用）
- Endpoint Controller：生成和维护同名server的所有endpoint（所有对应pod的service）
- Service Controller：监听、维护service的变化
- Namespace Controller
- ServiceAccount Controller
- Token Controller



## 代码机制

- client-go：负责与apiserver通信，获取API对象的状态信息
  - reflector维护与APIServer的连接，使用 ListAndWatcher方法来监听对象的变化，并把该变化事件及对应的API对象存入DeltaFIFO队列
  - Informer从DeltaFIFO取出API对象，根据事件的类型，来创建、更新或者删除本地缓存
  - Indexer使用线程安全的数据存储来缓存API对象及其值，为controller提供数据索引功能
  - Informer另一方面可以调用注册的Event Handler把API 对象发送给对应的controller
- custom controller：维护API对象的期望状态
  - 把事件对应的API对象存入workQueue中，这里存储的只是API对象的key
  - 进入Controller Loop：获取到API对象后则会根据API对象描述的期望状态与(集群)中的实际状态进行比对、协调，最终达到期望状态

![image-20200204184002547](figures/image-20200204184002547.png)