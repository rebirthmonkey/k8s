# Ingress Controller

## 简介

通常情况下，service 和 pod 的 IP 仅可在k8s集群内部访问，k8s集群外部的请求需要转发到 service 在 Node  上暴露的 NodePort 上，然后再由 kube-proxy 将其转发给相关的 Pod。而 Ingress 就是为进入k8s集群的请求提供路由规则的集合。Ingress是k8s内置的一个路由器，通过访问的URL把请求转发给不同的后端Service，所以ingress其实是为了代理不同后端Service而设置的路由服务。Ingress是L7的路由，而Service是L4的负载均衡，Ingress Controller基于Ingress规则将client的request直接转发到service对应的后端endpoint（即pod）上，这样会跳过kube-proxy的转发功能。

Ingres Controller以DaemonSet的形式创建，在每个node上以Pod hostPort的方式启动一个Nginx服务。它保持 watch Apiserver 的 /ingress 接口以更新 Ingress 资源，以满足 Ingress 的请求。

<img src="figures/image-20200810084318470.png" alt="image-20200810084318470" style="zoom: 25%;" />

### Ingress策略
一个Ingress对象可以有多个host，每个host里面可以有多个path对应多个service。Ingress策略定义的path需要与后端真实Service的path一致，否则将会转发到一个不存在的path上。Ingress策略定义的path需要与后端真实Service的path一致，否则将会转发到一个不存在的path上。

#### Host

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: test
spec:
  rules:
  - host: foo.bar.com
    http:
      paths:
      - backend:
          serviceName: s1
          servicePort: 80
  - host: bar.foo.com
    http:
      paths:
      - backend:
          serviceName: s2
          servicePort: 80
```

#### Path

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: test
spec:
  rules:
  - host: foo.bar.com
    http:
      paths:
      - path: /foo
        backend:
          serviceName: s1
          servicePort: 80
      - path: /bar
        backend:
          serviceName: s2
          servicePort: 80
```




## Nginx Ingress Controller
### Installation
```bash
helm install nginx-ingress-controller --namespace kube-system stable/nginx-ingress # ingress controller安装在localhost的80和443端口
```
- Check Installation
```bash
helm install svc1 ./svc1/chart
kubect get ingress -o wide # check if the backend endpoints are bound
vim /etc/hosts # xxx.com 127.0.0.1
curl -H 'Host:svc1.xxx.com' 127.0.0.1:80 # check the ingress
```
- Troubleshooting
```bash
kubectl exec -it -n kube-system nginx-ingress-controller-controller-57f69dc9b9-qf6gw -- cat /etc/nginx/nginx.conf
kubectl exec -it -n kube-system nginx-ingress-controller-controller-57f69dc9b9-qf6gw -- tail /var/log/nginx/error.log
```

### Labs 

#### Scenario 1: HTTP-Ingress-HTTP
- `kubectl apply -f ./svc1/ingress.yaml`: launch ingress, service and deployment
- `curl -H 'Host:svc1.xxx.com' http://127.0.0.1:80`

#### Scenario 2: HTTP-Ingress-HTTPS
- `kubectl apply -f ./svc2/ingress.yaml`: launch ingress, service and deployment
- `curl -H 'Host:svc2.xxx.com' http://127.0.0.1:80`

#### Scenario 3: HTTPS-Ingress-HTTP
- `kubectl apply -f ./svc1/ingress.yaml`: launch ingress, service and deployment
- `curl -H 'Host:svc1.xxx.com' http://127.0.0.1:80`

#### Scenario 4: HTTPS-Ingress-HTTPS(ssl-termination)
```bash
kubectl create secret tls secret-svc2 --key ./key.pem --cert ./cert.pem --dry-run

```
- `kubectl apply -f ./svc1/ingress.yaml`: launch ingress, service and deployment
- `curl -H 'Host:svc1.xxx.com' http://127.0.0.1:80`

#### Scenario 5: HTTPS-Ingress-HTTPS(ssl-passthrough)
- `kubectl apply -f ./svc1/ingress.yaml`: launch ingress, service and deployment
- `curl -H 'Host:svc1.xxx.com' http://127.0.0.1:80`



#### Scenario 5: TCP-Ingress-TCP（没测试）
- `kubectl apply -f ./svc3/ingress.yaml`: launch ingress, service and deployment
- `telnet svc3.xxx.com 32700`


## Ref
- [实践kubernetes ingress controller的四个例子](https://tonybai.com/2018/06/21/kubernetes-ingress-controller-practice-using-four-examples/)
- [HTTPS服务的Kubernetes ingress配置实践](https://tonybai.com/2018/06/25/the-kubernetes-ingress-practice-for-https-service/)

