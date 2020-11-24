# Basic
## Introduction

API对象是K8s集群中的管理操作单元。K8s集群系统每支持一项新功能，引入一项新技术，一定会新引入对应的API对象，支持对该功能的管理操作。例如副本集Replica Set对应的API对象是RS。

### YAML语法

每个API对象都有3大类属性：元数据metadata、规范spec和状态status。元数据是用来标识API对象的，每个对象都至少有3个元数据：namespace，name和uid；除此以外还有各种各样的标签labels用来标识和匹配不同的对象，例如用户可以用标签env来标识区分不同的服务部署环境，分别用env=dev、env=testing、env=production来标识开发、测试、生产的不同服务。规范描述了用户期望K8s集群中的分布式系统达到的理想状态（Desired State），例如用户可以通过复制控制器Replication  Controller设置期望的Pod副本数为3；status描述了系统实际当前达到的状态（Status），例如系统当前实际的Pod副本数为2；那么复本控制器当前的程序逻辑就是自动启动新的Pod，争取达到副本数为3。

K8s中所有的配置都是通过API对象的spec去设置的，也就是用户通过配置系统的理想状态来改变系统，这是k8s重要设计理念之一，即所有的操作都是声明式（Declarative）的而不是命令式（Imperative）的。声明式操作在分布式系统中的好处是稳定，不怕丢操作或运行多次，例如设置副本数为3的操作运行多次也还是一个结果，而给副本数加1的操作就不是声明式的，运行多次结果就错了。

k8s API对象的定义大多可以分为Metadata和Spec两个部分。前者存放对象的元数据，对所有API对象来说，这部分的字段和格式基本上是一致的。后者存放属于这个对象独有的定义，用来描述它所要表达的功能。

- metadata：元数据，它是API对象的“标识”，即从k8s里找到这个对象的主要依据
  - Labels：一组key-value格式的标签，表示对象的某些属性。Deployment使用label的过滤规则的Deployment的“spec.selector.matchLabels”字段，被称为Label Selector。
  - Annotations：携带key-value格式的内部信息，被k8s本身使用。多数Annotations都是自动被k8s加上的。
- spec：自定义数据

``` yaml
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
