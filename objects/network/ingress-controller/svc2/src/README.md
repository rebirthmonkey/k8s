# svc2

## Keys & Certificate Generation
### 服务器端公钥、私钥

```bash
openssl genrsa -out server.key 1024 # 生成服务器端私钥 
openssl rsa -in server.key -pubout -out server.pem # 生成服务器端公钥 
```

### 自签名 CA 证书

```bash
openssl genrsa -out ca.key 1024 # 生成 CA 私钥 
openssl req -new -key ca.key -out ca.csr # X.509 Certificate Request 
openssl x509 -req -in ca.csr -signkey ca.key -out ca.crt # X.509 self-signCertificate
```

在执行第二步时会出现：

```bash
1. ➜ keys openssl req -new -key ca.key -out ca.csr 
2. You are about to be asked to enter information that will be incorporated 
3. into your certificate request. 
4. What you are about to enter is what is called a Distinguished Name or a DN. 
5. There are quite a few fields but you can leave some blank 
6. For some fields there will be a default value, 
7. If you enter '.', the field will be left blank. 
8. \----- 
9. Country Name (2 letter code) [AU]:CN 
10. State or Province Name (full name) [Some-State]:Zhejiang 
11. Locality Name (eg, city) []:Hangzhou 
12. Organization Name (eg, company) [Internet Widgits Pty Ltd]:My CA 
13. Organizational Unit Name (eg, section) []: 
14. Common Name (e.g. server FQDN or YOUR name) []:localhost 
15. Email Address []: 
```

注意，这里的 `Organization Name (eg, company) [Internet Widgits Pty Ltd]:` 后面生成客户端和服务器端证书的时候也需要填写，不要写成一样的！！！可以随意写如：CAXXX。

然后 `Common Name (e.g. server FQDN or YOUR name) []:` 这一项，是最后可以访问的域名，我这里为了方便测试，写成 `localhost` ，如果是为了给我的网站生成证书，需要写成 `xxx.com` 。

### 服务器端证书

```bash
openssl req -new -key server.key -out server.csr # 服务器端在申请签名证书之前创建自己的 CSR 文件 
openssl x509 -req -CA ca.crt -CAkey ca.key -CAcreateserial -in server.csr -out server.crt # 向自己的 CA 机构申请证书，签名过程需要 CA 的证书和私钥参与，最终颁发一个带有 CA 签名的证书 
```

## Build Image
```bash
docker build -t wukongsun/nginx-ingress-demo-svc2:0.1 .
```

## Docker Test
```bash
docker run -d -p 30888:8080 wukongsun/nginx-ingress-demo-svc2:0.1
curl -k https://localhost:30888
```

## ks8 Test
```bash
kubectl apply -f service-node-port.yaml
curl -k https://localhost:30888
```