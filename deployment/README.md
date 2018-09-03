# ReplicaSet/ Deployment/ Job/ Cronjob/ StatefulSet
## ReplicaSet
ReplicaSet ensures a fixed number of running pods through selector which is the next generation of ReplicaController.
*It is recommended to be replaced by Deployment.*
- `kubectl create -t $REPLICASET_ID`: create replicaset
- `kubectl get replicasets`: list replicasets
- `kubectl delete replicasets $REPLICASET_ID`: delete replicaset
[ReplicaSet YAML example](replicaset.yaml)

### NodeSelector
- `kubectl label nodes NODE_ID zone=xxx`
- `vim rs.yaml`

    spec/containers/
      nodeSelector:
        zone: north  


## Deployment
Deployment instructs k8s how to create and update N pods through a ReplicaSet.
The main difference between RS and Deployment is that Deployment may 2 RS for rolling upgrade. 
- scaling: change the number of pod replicas in a deployment.
- docker image update
  - rolling update: create a new deploy to increase and decrease the old one
*Deployment doesn't handle the network access.*

- `kubectl get deployments`: list deployments
- `kubectl run nginx --image=IMG --port=80 --replicas=3`: create a deployment through a CMD
- `kubectl create -f DEP.yaml`: create a deployment through a YAML file
- `kubectl edit deployment DEP_ID`: edit deployment

### Scaling
- `kubectl scale deployments DEP_ID --replicas=4`: scale up

### Upgrade/ Rollout
- `kubectl rolling-update DPL_ID -f xxx-dpl.yaml`
- `kubectl set image deployment DEP_ID IMG_ID=nginx:latest`: upgrade image
- `kubectl rollout status deployment DEP_ID`: set rollout status

### TP
- `kubectl create -f deployment.yaml`: create a deployment with 2 replicas
- `kubectl get deployment`
- `kubectl describe DEP_ID`: to get IP address
- `curl POD_IP`: check the nginx server
- `kubectl scale deployment DEP_ID --replicas=3`: scale out
- `kubectl set image deployment DEP_ID IMG_ID=nginx:latest`: update image


## DaemonSet
Launch 1 pod on each node


## Job


## Cronjob


## StatefulSet
Stateful service with fix pod id and domain name
- stateful name: kafka
- fixed pod ID: kafka-0, kafka-1
- each pod uses PV/PVC
- bind with Headless service (without cluster IP) which maps directly to pod endpoints
- fixed domain name: kafka-0.kafka, kafka-1.kafka