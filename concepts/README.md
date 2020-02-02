# Basic
## API Groups
k8s has several API groups and resource objects belong to one of these API groups:
- core (also called legacy) group: for standard resource objects like pod 
  - REST path `/api/v1` is not specified as part of the apiVersion field, for example `apiVersion: v1`
  - pod, service...
- named groups: for new resource objects
  - REST path `/apis/$GROUP_NAME/$VERSION` and uses `apiVersion: $GROUP_NAME/$VERSION`  like `apiVersion: batch/v1`
  - `apps` API group: StatefulSet
  - `extension` API group: 


## Object Resources
- [Pod](pod/README.md)
- [Workload](workload/README.md)
- [Service](service/README.md)
- [Storage including Volume, Persistent Volume/ PVC, ConfigMap, Secret](storage/README.md)
- [Network including Ingress](network/README.md)
