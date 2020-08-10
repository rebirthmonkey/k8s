# Workload
## ReplicaSet
ReplicaSet ensures a fixed number of running pods through selector.
*It is recommended to be replaced by Deployment.*

### Labels

- metadata/labels：给上层deployment使用的label
- spec/selector/matchLabels：筛选pod（spec/template/metadata/labels）的label

### CMD

- `kubectl apply -t replicaset1.yaml`: create replicaset
- `kubectl get replicasets`: list replicasets
- `kubectl delete replicasets $REPLICASET_ID`: delete replicaset

### NodeSelector
- `kubectl label nodes NODE_ID zone=xxx`
- `vim replicaset2-node-selector.yaml`


## Deployment
部署表示用户对K8s集群的一次更新操作。部署是一个比RS应用模式更广的API对象，可以是创建一个新的服务，更新一个新的服务，也可以是滚动升级一个服务。滚动升级一个服务，实际是创建一个新的RS，然后逐渐将新RS中副本数增加到理想状态，将旧RS中的副本数减小到0的复合操作；这样一个复合操作用一个RS是不太好描述的，所以用一个更通用的Deployment来描述。以K8s的发展方向，未来对所有长期伺服型的的业务的管理，都会通过Deployment来管理。

### Label
- metadata/labels：给上层service使用的label
- spec/selector/matchLabels：
  - replicaSet/metadata/labels使用的label
  - 筛选pod（spec/template/metadata/labels）的label
  - 后面service用到的deployment的label：**必须与selector的label相同**

### CMD
- list deployments
  - `kubectl get deployments`
- create
  - `kubectl run DEP_NAME --image=IMG_NAME --image-pull-policy=IfNotPresent --port=80 --replicas=3`
  - `kubectl apply -f DEP.yaml`: create a deployment through a YAML file
- edit
  - `kubectl edit deployment DEP_ID`: edit deployment
- delete
  - `kubectl delete deployment DEP_ID`
- upgrade/rollout
  - `kubectl set image deployment DEP_ID CT_ID=IMG_ID --record`: upgrade image，并且通过record来记录
    -  `kubectl set image deployment nginx-deployment nginx=nginx:latest --record`
  - `kubectl rollout history deployment DEP_ID`: list all the revision
    - `kubectl rollout history deployment DEP_ID --revision=1`: detail the revision
  - `kubectl rollout status deployment DEP_ID`: show rollout operation status
  - `kubectl roolout undo deployment DEP_ID --to-revision=4`: switch to revision 4
  - `kubectl rolling-update DPL_ID -f xxx-dpl.yaml`
- scaling
  - `kubectl scale deployments DEP_ID --replicas=4`: scale up
- autoscale
  - `kubectl autoscale deployments DEP_ID --min=3 --max=5 --cpu-percent=10`

### Labs

#### Deployment by CMD
- `kubectl run dep-nginx --image=nginx:1.9.0 --image-pull-policy=IfNotPresent --replicas=2`

#### Scale & upgrade
- `kubectl create -f deployment1.yaml`: create a deployment with 2 replicas
- `kubectl get deployment`
- `kubectl get pods -o wide`: get pod IPd
- `curl POD_IP`: check the Nginx server
- `kubectl scale deployment DEP_ID --replicas=3`: scale out
- `kubectl set image deployment deployment1 nginx=nginx:stable --record`: upgrade image
- `kubectl get pods -o wide`
- `kubectl rollout history deployment deployment1`
- `kubectl rollout history deployment deployment1 --revision=1`
- `kubectl rollout undo deployment deployment1 --to-revision=1`

#### HPA
The **metric-server** should be installed.
- `kubectl apply -f deployement2-hpa.yaml`
- `kubectl autoscale deployments deployment2-hpa --min=1 --max=5 --cpu-percent=10`
- `kubectl run -it --rm load-generator --image=busybox /bin/sh`
  - `while true; do wget -q -O- http://deployment2-hpa-service; done`


## DaemonSet
长期伺服型和批处理型服务的核心在业务应用，可能有些节点运行多个同类业务的Pod，有些节点上又没有这类Pod运行；而后台支撑型服务的核心关注点在K8s集群中的节点（物理机或虚拟机），要保证每个节点上都有一个此类Pod运行。节点可能是所有集群节点也可能是通过nodeSelector选定的一些特定节点。典型的后台支撑型服务包括，存储，日志和监控等在每个节点上支撑K8s集群运行的服务。

### Train & Toleration
```yaml
  tolerations:
  - key: node-role.kubernetes.io/master
    effect: NoSchedule
```
tolerate the `NoSchedule` of the master  

### CMD
- `kubectl taint node docker-desktop node-role.kubernetes.io/master=:NoSchedule`：taint可以key、effect而没有value
- `kubectl apply -f deployment1.yaml`：pod一直属于pending状态，无法调度
- `kubectl apply -f daemonset.yaml`
- `kubectl get pods -o wide`

## Job

Job是K8s用来控制批处理型任务的API对象。批处理业务与长期伺服业务的主要区别是批处理业务的运行有头有尾，而长期伺服业务在用户不停止的情况下永远运行。Job管理的Pod根据用户的设置把任务成功完成就自动退出了。成功完成的标志根据不同的spec.completions策略而不同：单Pod型任务有一个Pod成功就标志完成；定数成功型任务保证有N个任务全部成功；工作队列型任务根据应用确认的全局成功而标志成功。

### 重启策略
- never
- OnFailure

### Lab
#### Simple Job
- `kubectl apply -f job1.yaml`
- `kubectl get job`
- `kubectl logs job1-xxxx`

#### Completion Job
Job会启动多个pod完成completion
- completions: 总共需要执行job的次数
- parallelism: 并行执行job的数梁
- `kubectl apply -f job2-completion.yaml`
- `kubectl get pod -w`
- `kubectl get job.batch`


#### Cronjob
CronJob即定时任务，就类似于Linux系统的crontab，在指定的时间周期运行指定的任务。使用CronJob需要开启batch/v2alpha1 API，

•.spec.schedule指定任务运行周期，格式同Cron                 分  时  日  月  周
•.spec.jobTemplate指定需要运行的任务，格式同Job
•.spec.startingDeadlineSeconds指定任务开始的截止期限
•.spec.concurrencyPolicy指定任务的并发策略，支持Allow、Forbid和Replace三个选项

- `kubectl apply -f cronjob1.yaml`
- `kubectl get cronjobs.batch`
- `kubectl logs cronjob1-1542784380-ggdqn`

## StatefulSet

在云原生应用的体系里，有下面两组近义词；第一组是无状态（stateless）、牲畜（cattle）、无名（nameless）、可丢弃（disposable）；第二组是有状态（stateful）、宠物（pet）、有名（having  name）、不可丢弃（non-disposable）。RC和RS主要是控制提供无状态服务的，其所控制的Pod的名字是随机设置的，一个Pod出故障了就被丢弃掉，在另一个地方重启一个新的Pod，名字变了、名字和启动在哪儿都不重要，重要的只是Pod总数；而StatefulSet是用来控制有状态服务，StatefulSet中的每个Pod的名字都是事先确定的，不能更改。StatefulSet中Pod的名字的作用，是关联与该Pod对应的状态。

对于RC和RS中的Pod，一般不挂载存储或者挂载共享存储，保存的是所有Pod共享的状态，Pod像牲畜一样没有分别；对于StatefulSet中的Pod，每个Pod挂载自己独立的存储，如果一个Pod出现故障，从其他节点启动一个同样名字的Pod，要挂载上原来Pod的存储继续以它的状态提供服务。

适合于StatefulSet的业务包括数据库服务MySQL和PostgreSQL，集群化管理服务Zookeeper、etcd等有状态服务。StatefulSet的另一种典型应用场景是作为一种比普通容器更稳定可靠的模拟虚拟机的机制。传统的虚拟机正是一种有状态的宠物，运维人员需要不断地维护它，容器刚开始流行时，我们用容器来模拟虚拟机使用，所有状态都保存在容器里，而这已被证明是非常不安全、不可靠的。使用StatefulSet，Pod仍然可以通过漂移到不同节点提供高可用，而存储也可以通过外挂的存储来提供高可靠性，StatefulSet做的只是将确定的Pod与确定的存储关联起来保证状态的连续性。StatefulSet还只在Alpha阶段，后面的设计如何演变，我们还要继续观察。



