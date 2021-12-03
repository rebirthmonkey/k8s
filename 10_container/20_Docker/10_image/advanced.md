# Advanced Topic for Docker Image

## Local Docker Registry

- `docker run -d --name tshift-xgw-registry --restart always -p 38008:5000 -v /data/registry-data:/var/lib/registry registry:2.5.2`: run a local Docker registry

### 使用Http Registry

- `vi /usr/lib/systemd/system/docker.service`: 使docker pull支持http insecure registry协议

  ```
  ExecStart=/usr/bin/dockerd --insecure-registry 127.0.0.1:38008
  ```

- `vi /etc/docker/daemon.json`

  ```
  {
    "registry-mirrors": ["https://10.123.97.147"],  
    "max-concurrent-downloads": 6,
    "insecure-registries" : ["docker-registry.tshift-test.oa.com"] 
  }
  ```

### Manipulation

- `curl -X GET https://myregistry:5000/v2/_catalog`: list image of the registry

### Upload Image

如果是dockerhub上缺省的image，需要放在*library*目录下！

- `docker tag registry:2.5.2 127.0.0.1:38008/library/registry:2.5.2`
- `docker push 127.0.0.1:38008/library/registry:2.5.2`