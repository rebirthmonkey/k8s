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
Deployment instructs k8s how to create and update N pods through a ReplicaSet.
The main difference between rs and dpl is that dpl may use 2 rs for rolling upgrade. 
- scaling: change the number of pod replicas in a deployment.
- docker image update
  - rolling update: create a new deploy to increase and decrease the old one
*Deployment doesn't handle the network access.*

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
Launch 1 pod on each node

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
Stateful service with fix pod id and domain name
- stateful name: kafka
- fixed pod ID: kafka-0, kafka-1
- each pod uses PV/PVC
- bind with Headless service (without cluster IP) which maps directly to pod endpoints
- fixed domain name: kafka-0.kafka, kafka-1.kafka

