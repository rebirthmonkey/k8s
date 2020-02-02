# Docker Concepts



## Components

![Docker Main Components](figures/docker-architecture.png)

- Docker client: send commands
- Docker Daemon: server to handle requests
  - `/etc/systemd/system/multi-user.target.wants/docker.serivce` `-H tcp://0.0.0.0`: configuration to accept remote requests (no need to do)
  - `systemctl daemon-reload` and `systemctl restart docker.service`
  - `docker -H 192.168.88.8 info`: example (no need to do)
- Registry: host Docker images

## Basics

- [namespace](namespace.md)
- [cgroup](cgroup.md)