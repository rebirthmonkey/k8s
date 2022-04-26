FROM centos:7

RUN yum update -y \
    && yum install -y iptables \
    && yum clean all

RUN mkdir -p /data && groupadd docker
ADD ["./files/docker.tar.xz", "/usr/local/bin/"]
COPY ["./scripts/init.sh", "/data/init.sh"]
RUN chmod +x /data/init.sh

CMD ["/data/init.sh"]
