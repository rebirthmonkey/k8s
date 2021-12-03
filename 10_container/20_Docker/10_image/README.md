# Image

## Introduction

### Image Layer Concept

<img src="figures/image-kernel-0609074.png" alt="Image Kernel Architecture" style="zoom:33%;" />

- bootfs: the kernel on the host to be shared by all the containers
  - `uname -r` on the host and in the container: the same kernel info
- rootfs: each container's userspace filesystem, it includes /dev, /proc, /bin

<img src="figures/image-multi-containers-0609074.png" alt="Multiple Containers upon the same kernel" style="zoom:33%;" /> 

- image contains multiple layers which are mutable
- container layer: only the top layer is a writable layer corresponds to a container 

<img src="figures/image-multiple-layers-0609074.png" alt="Image Multiple Layer" style="zoom:33%;" />

### 镜像下载

#### 镜像完整路径

``<registry>/<repository>/<image>:<tag>``

#### 下载流程
- 下载Manifest：`GET /v2/<name>manifests/<reference>`，从而获得分层镜像列表
- 分层下载镜像：`GET /v2/<name>/blobs/<blobsum>`


## Manipulation
- `docker image ls`: list all images in the local registry
  - `docker image ls -q`: display only image ID 
- `docker search ubuntu:xenial`: search all images from the remote registry
- `docker image pull <repository>:<tag>`: download an image from the remote registry to the local registry
  - `docker image pull <repository>`: if we don't specify an image tag, Docker uses `latest` as default tag
  - `docker image pull -a <repository>`: download all the images of the repo  
  - `docker image pull gcr.io/nigelpoulton/tu-demo:v2`: download from a third-party registry
- `docker image inspect ubuntu:xenial`: inspect an image
- `docker image rm IMG_ID`: remove a local image
  - `docker image rm $(docker image ls -q) -f`: delete all images on the host
- `docker history IMG_ID`: display all the layers of an image


## tag
- `docker image tag OLD_REPO:ODL_TAG NEW_REPO:NEW_TAG`: change the tag of an image


## create/commit/push
- create an account in `hub.docker.com`, my account is **wukongsun**
- `docker container commit -m <comment> -a <author> CT_ID REPO:TAG`: create an image from a running container
- push to a remote registry
  - `docker login`: login to `hub.docker.com`
  - `docker image push REPO:TAG`: upload to the remote registry 


## import/export
- `docker save REPO:TAG > /tmp/registry.tar`: export the registry image
- `docker load < registry.tar`: import the registry image


## Lab

- Download ubuntu:xenial image

```shell
docker image ls
docker search ubuntu:xenial
docker pull ubuntu:xenial
docker image ls
docker ps -a
```

- Create a Ubuntu:Xenial Image with ifconfig

```shell
docker run -it --rm ubuntu:xenial /bin/bash
```
- in this container terminal, run:
```shell
ping 8.8.8.8 # it doesn't work since it doesn't have the ping tool
apt update
apt install iputils-ping iproute2
ping 8.8.8.8 # it works now!
```
- from another terminal, run
```shell
docker ps # find docker ID `CT_ID`
```
  - push the new image to DockerHub
```shell
docker commit -m "xenial with ping" -a "USER_NAME" CT_ID ACCOUNT/xenial:net
docker login
docker image push ACCOUNT/xenial:net
docker image tag ACCOUNT/xenial:net xenial:net
```

