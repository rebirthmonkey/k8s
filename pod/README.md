# Pod
## Introduction
Atomic unit in k8s, *it always runs on 1 node*.
- computing: 1 or N containers, but the number of containers within 1 pod is fixed
- storage: all containers in 1 pod have the same mount point, can access the same shared volume
- networking: all the containers in 1 pod use a unique IP address, communicate with one another using `localhost`
- scalability: increase or decrease the number of pods

### Storage
pod-level storage which will be deleted when pod is destroyed.  
- emptyDir
- hostPath
- configMap
- secret

### Network
- hostPort: container level, expose 1 containerPort on the host

      ports: 
      - containerPort: 8080
        hostPort: 8081

- hostNetwork: pod level, expose all the containerPorts on the host

      hostNetwork: true


### Health Check
- livenessProbe:
  - exec:
  - tcpSocket:
  - httpGet:
  - initialDelaySeconds (s):
  - timeoutSeconds (s): 
- readinessProbe: 

### initContainer
只有当所有的initContainer都运行完之后，才会初始化containers
- `vim dpl.yaml`

    spec:
      initContainers:
      containers:

### Static Pod
Pod only exists on a node, managed by the local kubelet.  
It cannot be managed by the API server, so it cannot be managed by ReplicationController, Deployment or DaemonSet.
- launched by the config file */etc/kubelet.d/*
- launched by HTTP 

## Usage
CMD
- `kubectl get pods`: list pods
  - `keubctl get pods --show-all`
- `kubectl describe pods`: describe pods
- `kubectl create -f POD.yml`: launch a pod
- `kubectl delete pod POD_ID` or `kubectl delete -f POD.yml`: delete pod
- `kubectl exec POD_ID -- CMD`: run a cmd in the 1st CT of the pod
  - `kubectl exec POD_ID curl localhost:8080`: internal access
  - `kubectl exec POD_ID -c CT_ID -- CMD `: run a cmd in one CT of the pod

### ConfigMap
- ENV: get 1 value from ConfigMap *Spec/Containers/env*

      name: APPLOGLEVEL     # environment variable name
      valueFrom: 
        configMapKeyRef: 
          name: cm-appvars
          key: apploglevel

- ENV: get all values from ConfigMap: *Spec/Containers/env*

      envFrom: 
        configMapRef: 
          name: cm-appvars

- volumeMount: *spec/containers/volumeMounts*

      name: serverxml       # volume name
      mountPath: /configfiles
      
      volumes: 
      - name: severxml
       configMap: 
         name: cm-appconfigfiles
         items: 
         - key: key-severxml
           path: sever.xml
         - key: key-loggingproperties
           path: logging.properties


### Downward API
- ENV: get pod info from field *Spec/Containers/env*

      name: MY_POD_NAME     # environment variable name
      valueFrom: 
        fieldRef: 
          fieldRef: metadata.name
          
  - metadata: fixed info about a pod 
    - metadata.name
    - metadata.namespace 
  - status: variable info about a pod
    - status.podIP

- ENV: get container info from resourceField *Spec/Containers/env*

      name: MY_CPU_REQUEST     # environment variable name
      valueFrom: 
        resourceFieldRef: 
          containerName: test-container
          resource: requests.cpu
  - requests.cpu
  - requests.memory
  - limits.cpu
  - limits.memory  
- volume: *volumes*

      - name: podinfo
        downwardAPI:
          items: 
            - path: "labels" # create a file called "labels"
              fieldRef: 
                fieldPath: metadata.labels      # all the labels of in the metadata
  
## Build Image
- Program in the container should be run on the frontend


## Example
### 1 Pod with 1 Container
- `kubectl create -f pod1.yaml`
- `kubectl exec -it pod1 -- env`
- `kubectl exec -it pod1 -- /bin/sh`
- `kubectl describe pod pod1`: get IP address
- `ping POD1_IP`: can ping pod1

### 1 Pod with 2 Containers
- `kubectl create -f pod2.yaml`
- `kubectl exec -it pod2 -c ct-nginx -- /bin/bash`
  - `apt-get update`
  - `apt-get install curl`
  - `curl localhost`: get the hello message from the container
- `kubectl describe pod pod2`: get IP address
- `curl POD2_IP`: get the hello message from the node
- `kubectl exec -it pod2 -c ct-debian -- /bin/bash`
  - `echo Chanage message from pod2-ct-busybox > /data/index.html `
- `curl POD2_IP`: get the new message from the node
