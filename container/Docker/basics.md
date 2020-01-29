# Docker操作

## 基础

Docker创建一个 " 容器进程 "时，会先创建的一个容器初始化进程 (dockerinit)，而不是应用进程 (ENTRYPOINT + CMD)。dockerinit会负责完成根目录的准备、挂载设备和目录、配置hostname等一系列需要在容器内进行的初始化操作。最后，它通过execv()系统调用，让应用进程取代自己，成为容器里的PID=1的进程。

### run





### exec

docker exec的原理是启动一个进程，将其加入到某个进程已有的namespace中，从而达到“进入”这个进程所在容器的目的。

```
$ docker inspect --format '{{ .State.Pid }}' 
4ddf4638572d25686
$ ls -l /proc/25686/ns
total 0
lrwxrwxrwx 1 root root 0 Aug 13 14:05 cgroup -> cgroup:[4026531835]lrwxrwxrwx 1 root root 0 Aug 13 14:05 ipc -> ipc:[4026532278]lrwxrwxrwx 1 root root 0 Aug 13 14:05 mnt -> mnt:[4026532276]lrwxrwxrwx 1 root root 0 Aug 13 14:05 net -> net:[4026532281]lrwxrwxrwx 1 root root 0 Aug 13 14:05 pid -> pid:[4026532279]lrwxrwxrwx 1 root root 0 Aug 13 14:05 pid_for_children -> pid:[4026532279]lrwxrwxrwx 1 root root 0 Aug 13 14:05 user -> user:[4026531837]lrwxrwxrwx 1 root root 0 Aug 13 14:05 uts -> uts:[4026532277]
```


