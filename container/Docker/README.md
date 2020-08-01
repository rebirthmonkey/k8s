# Docker Tutorial

## Installation

- [Docker Installation](operation/installation.md)


## Conception
![Docker Main Components](/Users/ruan/workspace/k8s/container/Docker/figures/docker-architecture-6272685.png)

- Docker client: send commands
- Docker Daemon: server to handle requests
  - `/etc/systemd/system/multi-user.target.wants/docker.serivce` `-H tcp://0.0.0.0`: configuration to accept remote requests (no need to do)
  - `systemctl daemon-reload` and `systemctl restart docker.service`
  - `docker -H 192.168.88.8 info`: example (no need to do)
- Registry: host Docker images


## Image
- [image](image/README.md)


## Runtime
- [runtime](runtime/README.md)


## Volume
- [volume](volume/README.md)


## Network
- [network](network/README.md)


## Dockerfile
- [Dockerfile](dockerfile/README.md)


## Docker-compose
- [Docker-compose](docker-compose/README.md)


## Lab
- [Lab](lab/README.md)
