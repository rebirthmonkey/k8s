# Ingress Controller

## 简介

Ingress是k8s内置的一个路由器，通过访问的URL把请求转发给不同的后端Service，所以ingress其实是为了代理不同后端Service而设置的路由服务。Ingress是L7的路由，而Service是L4的负载均衡，Ingress Controller基于Ingress规则将client的request直接转发到service对应的后端endpoint（即pod）上，这样会跳过kube-proxy的转发功能。

Ingres Controller以DaemonSet的形式创建，在每个node上启动以Pod hostPort的方式一个Nginx服务。

### Ingress策略
一个Ingress对象可以有多个host，每个host里面可以有多个path对应多个service。Ingress策略定义的path需要与后端真实Service的path一致，否则将会转发到一个不存在的path上。Ingress策略定义的path需要与后端真实Service的path一致，否则将会转发到一个不存在的path上。

- host：
- path


## Nginx Ingress Controller
### Installation
- `helm install nginx-ingress-controller --namespace kube-system stable/nginx-ingress`：ingress controller安装在localhost的80和443端口
- Check Installation
  - `helm install svc0 ./svc0`
  - `kubect get ingress -o wide`: check if the backend endpoints are bound
  - `vim /etc/hosts`
    - xxx.com 127.0.0.1
  - `curl -H 'Host:svc0.xxx.com' 127.0.0.1:80`: check the ingress
- Troubleshooting
  - `kubectl exec -it -n kube-system nginx-ingress-controller-controller-57f69dc9b9-qf6gw -- cat /etc/nginx/nginx.conf`
  - `kubectl exec -it -n kube-system nginx-ingress-controller-controller-57f69dc9b9-qf6gw -- tail /var/log/nginx/error.log`

### Labs 

![image-20200806095527275](figures/image-20200806095527275.png)

#### Scenario 1: 1 Ingress Controller, 1 HTTP Ingress, 1 HTTP Service
- `helm install --name svc1 ./svc1`: launch ingress, service and deployment
- `curl -H 'Host:svc1.xxx.com' http://127.0.0.1:80`

#### Scenario 2: 1 Ingress Controller, 1 HTTP Ingress, 1 HTTPS Service
- `helm install --name svc2 ./svc2`: launch ingress, service and deployment
- `curl -H 'Host:svc2.xxx.com' http://127.0.0.1:80`

#### Scenario 3: 1 Ingress Controller, 1 HTTP Ingress, 1 TCP Service（没测试）
- `helm install --name svc3 ./svc3`: launch ingress, service and deployment
- `telnet svc3.xxx.com 32700`

#### Scenario 4: 2 Ingress Controller, 6 Ingress (2 HTTP, 2 HTTPS, 2 TCP)（没测试）
- `helm install --name svc4 ./svc4`
- `curl -H 'Host:svc4.tonybai.com' http://127.0.0.1:32700`
- `helm install --name svc5 ./svc5`
- `curl -H 'Host:svc5.tonybai.com' http://127.0.0.1:32700`
- `helm install --name svc6 ./svc6`
- `telnet svc6.tonybai.com 32700`

#### Scenario 5: 1 Ingress Controller, 1 HTTPS Ingress, 1 HTTP Service
- `kubectl create secret tls ingress-controller-demo-tls-secret --key server.key --cert server.crt`
- `helm install --name svc7 ./svc7`
- `curl -k -H 'Host:svc7.xxx.com' https://127.0.0.1:32701`

#### Scenario 6: 1 Ingress Controller, 1 HTTPS Ingress, 1 HTTPS Service (ssl-termination)
- `helm install --name svc8 ./svc8`
- `curl -k -H 'Host:svc8.xxx.com' https://127.0.0.1:32701`

#### Scenario 7: 1 Ingress Controller, 1 HTTPS Ingress, 1 HTTPS Service (ssl-passthrough)
ssl-passthrough这个无法通过
- `helm install --name svc9 ./svc9`
- `curl -k --key ./client.key --cert ./client.crt -H 'Host:svc9.xxx.com' https://127.0.0.1:32701`


## Ref
- [实践kubernetes ingress controller的四个例子](https://tonybai.com/2018/06/21/kubernetes-ingress-controller-practice-using-four-examples/)
- [HTTPS服务的Kubernetes ingress配置实践](https://tonybai.com/2018/06/25/the-kubernetes-ingress-practice-for-https-service/)

