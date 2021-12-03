# Docker Tutorial

## Conception

<img src="./figures/docker-architecture.png" alt="Docker Main Components" style="zoom: 50%;" />

- Docker client: send commands
- Docker Daemon: server to handle requests

```shell
/etc/systemd/system/multi-user.target.wants/docker.serivce -H tcp://0.0.0.0 #  configuration to accept remote requests (no need to do)
systemctl daemon-reload
systemctl restart docker.service
docker -H 192.168.88.8 info # example (no need to do)
```

- Registry: host Docker images

## Image
- [image](10_image/README.md)


## Runtime
- [runtime](15_runtime/README.md)


## Volume
- [volume](20_volume/README.md)


## Network
- [network](25_network/README.md)


## Dockerfile
- [Dockerfile](30_dockerfile/README.md)


## Lab
- [Lab](80_lab/README.md)


## Advanced Topics
- [Advanced Topics](90_topics/README.md)

