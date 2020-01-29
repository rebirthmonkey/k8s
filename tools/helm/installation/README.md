# Helm
## 离线部署
版本: v2.9.1
- `cd /data`
- `wget http://openstack.oa.com/tshift/helm-v2.9.1-linux-amd64.tar.gz`: download Helm client
- `docker pull docker-registry.tshift-test.oa.com/tiller:v2.9.1`: download Helm Tiller
- `yum install -y socat`
- `tar -zxvf helm-v2.9.1-linux-amd64.tar.gz`
- `mv linux-amd64/helm /usr/local/bin/helm`: install Helm client
- `helm init --tiller-image tiller:v2.9.1 --skip-refresh`

## 测试
- `docker pull nginx:1.15`
- `helm create hello-helm`
- `helm install ./hello-helm`
- `export POD_NAME=$(kubectl get pods --namespace default -l "app=hello-helm,release=fallacious-snail" -o jsonpath="{.items[0].metadata.name}")`
- `kubectl port-forward $POD_NAME 8080:80`
- `echo "Visit http://127.0.0.1:8080 to use your application"`
        