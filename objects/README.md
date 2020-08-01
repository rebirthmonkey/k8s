# Basic
## Introduction

### YAML语法

k8s API对象的定义大多可以分为Metadata和Spec两个部分。前者存放对象的元数据，对所有API对象来说，这部分的字段和格式基本上是一致的。后者存放属于这个对象独有的定义，用来描述它所要表达的功能。

- metadata：元数据，它是API对象的“标识”，即从k8s里找到这个对象的主要依据
  - Labels：一组key-value格式的标签，表示对象的某些属性。Deployment使用label的过滤规则的Deployment的“spec.selector.matchLabels”字段，被称为Label Selector。
  - Annotations：携带key-value格式的内部信息，被k8s本身使用。多数Annotations都是自动被k8s加上的。
- spec：自定义数据

```yaml
apiVersion: apps/v1
kind: Deployment
metadata: 
	name: nginx-deployment
spec: 
	selector: 
		matchLabels: 
			app: nginx 
	replicas: 2 
	template: 
		metadata: 
			labels: 
				app: nginx 
		spec: 
			containers: 
			- name: nginx 
				image: nginx:1.7.9 
				ports: 
				- containerPort: 80
```

## Object Resources

- [Pod](pod/README.md)
- [Workload](workload/README.md)
- [Service](service/README.md)
- [Storage including Volume, Persistent Volume/ PVC, ConfigMap, Secret](storage/README.md)
- [Network including Ingress](network/README.md)
