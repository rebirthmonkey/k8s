# DinD

A detailed description can be found [here](http://blog.teracy.com/2017/09/11/how-to-use-docker-in-docker-dind-and-docker-outside-of-docker-dood-for-local-ci-testing/)

## Dockerfile

```yaml
FROM centos:7

RUN yum update -y \
    && yum install -y iptables \
    && yum clean all

RUN mkdir -p /data && groupadd docker
ADD ["./files/docker.tar.xz", "/usr/local/bin/"]
COPY ["./scripts/init.sh", "/data/init.sh"]
RUN chmod +x /data/init.sh

CMD ["/data/init.sh"]
```

## Build & Run Container

- `cd dind/`
- `docker build -t centos:7-dind -f Dockerfile .`
- `docker run --privileged -d --name dind centos:7-dind`
