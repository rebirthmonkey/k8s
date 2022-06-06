# 其他

### proxy

- 创建

```shell
kubectl proxy
```

- 验证：list

```shell
curl -iv http://127.0.0.1:8001/api/v1/namespaces/default/pods
```

- 验证：watch

```shell
curl -iv http://127.0.0.1:8001/api/v1/namespaces/default/pods\?watch\=true
```