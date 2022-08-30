# Docker Runtime

## 简介

Docker 创建一个“容器进程”时，会先创建的一个容器初始化进程（dockerinit），而不是应用进程 （ENTRYPOINT + CMD）。dockerinit 会负责完成根目录的准备、挂载设备和目录、配置 hostname 等一系列需要在容器内进行的初始化操作。最后，它通过 execv() 系统调用，让应用进程取代自己，成为容器里的 PID=1 的进程。

## Manipulation

### ps/inspect

- `docker ps`
  - `docker ps -a`: list all the containers included the killed
  
- `docker inspect`
  - `docker inspect --format ‘{{ .State.Pid }}’<container-id>`

### run

#### Run

- `docker run ubuntu:focal /bin/bash`: tell Docker which process to run inside container to replace default CMD, but nothing can be shown in the terminal
- `docker run -it ubuntu:focal`: interactive mode, connect your terminal to the CT's bash shell
  - `Ctrl-PQ`: exist and suspend the container
- `docker run --name CT_Name ubuntu:focal`: name of the container
- `docker run -it -d ubuntu:focal`: detached mode (executing as daemon in background)
  - `docker attach CT_ID`: attach to the detached container, should input "ENTER"
- `docker run -it --rm ubuntu:focal`: remove after the execution
- `docker run -d -p 80:80 ubuntu:focal`: NAT the port
- `docker run -d -P ubuntu:focal`: NAT port of the container to a random port of the host

#### Resource Limitation

- `docker run -m 200M --memory-swap=300M ubuntu:focal`
  - `-m 200M`: memory
  - `--memory-swap 300M`: memory+swap
- `docker run -it --vm 1 --vm-bytes 280M ubuntu:focal`
  - `--vm 1`: 1 process for the container
  - `--vm-bytes 280M`: 280M memory for the process
- `docker run -c 1024 ubuntu:focal`
  - `-c 1024`: CPU priority
- `docker run -it --blkio-weight 600 ubuntu:focal`
  - `--blkio-weight 600`: disk input/output priority

### attach/exec

docker exec 的原理是启动一个进程，将其加入到某个进程已有的 namespace 中，从而达到“进入”这个进程所在容器的目的。

```bash
$ docker inspect --format '{{ .State.Pid }}' 
4ddf4638572d25686
$ ls -l /proc/25686/ns
total 0
lrwxrwxrwx 1 root root 0 Aug 13 14:05 cgroup -> cgroup:[4026531835]lrwxrwxrwx 1 root root 0 Aug 13 14:05 ipc -> ipc:[4026532278]lrwxrwxrwx 1 root root 0 Aug 13 14:05 mnt -> mnt:[4026532276]lrwxrwxrwx 1 root root 0 Aug 13 14:05 net -> net:[4026532281]lrwxrwxrwx 1 root root 0 Aug 13 14:05 pid -> pid:[4026532279]lrwxrwxrwx 1 root root 0 Aug 13 14:05 pid_for_children -> pid:[4026532279]lrwxrwxrwx 1 root root 0 Aug 13 14:05 user -> user:[4026531837]lrwxrwxrwx 1 root root 0 Aug 13 14:05 uts -> uts:[4026532277]
```

- `docker attach`: attach to the container's terminal
  - `docker attach CT_ID`
- `docker exec`: run a new process inside the container
  - `docker exec –it CT_ID /bin/bash`: it attaches a running container with a bash

### stop/kill/start/restart/rm

- `docker start CT_ID`: restart
- `docker stop CT_ID`: stop (send SIGTERM + SIGKILL)
- `docker kill CT_ID`: kill (send SIGKILL)
- `docker rm CT_ID`: remove a *stopped* container
    - `docker rm -f CT_ID`: force mode, remove a *running* container
    - `docker rm -f $(docker container ps -aq)`: remove all the containers

### pause/unpause

- `docker pause CT_ID`
- `docker unpause CT_ID`

### monitor

- `docker ps`
- `docker container top CT_ID`: real-time monitor
- `docker logs CT_ID`: display logs inside a container
- `docker logs -f CT_ID`: continue to display new logs

## Lab

### Basic

``` shell
docker run hello-world 
docker ps # we can't see the container `hello-world`
docker ps -a # we can see all the containers including the stopped containers
docker run -it --rm ubuntu:focal /bin/bash
```

from another terminal

```shell
docker container ps # what's the difference between the previous case? Why?
```

in the container

```shell
ps aux
exit # `Ctrl-PQ`: exit the container
docker ps -a
docker exec -it CT_ID /bin/bash
```

### Run a Web Server

```shell
docker container run -it --rm -p 8888:80 ubuntu:focal
```

install and launch apache2 in the container

```shell
apt update
apt install apache2 vim
vim /var/www/html/index.html # edit the file 
apache2ctl -D FOREGROUND 
```

on the host

```shell
curl localhost:8888 # access the web page
```

## Bug

### 外部无法连接容器

容器内必须绑定 0.0.0.0，而非 127.0.0.1。
