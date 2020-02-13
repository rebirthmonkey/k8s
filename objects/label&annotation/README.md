# Label & Annotation

## Label
Labels are key-value pairs that are used to group together sets of objects, very often pods.

- show labels：
  - `kubectl get pods --show-labels`
- Add label
  - `kubectl label pod POD_ID app=v1`
  - `kubectl label node node02 node-role.kubernetes.is/node=`: `node-role.kubernetes.is/node`为key
- select label
  - `kubectl get pods -l run=kubernetes-bootcamp`: select with label `run=kubernetes-bootcamp`
  - `kubectl get services -l run=kubernetes-bootcamp`: select with label `run=kubernetes-bootcamp`


## Annotation
Annotations let you associate arbitrary metadata with k8s objects. 

