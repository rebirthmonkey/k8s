# Storage



## Volume

Docker中的Volume机制允许你将宿主机上指定的目录或者文件，挂载到容器里面进行读取和修改操作。

当容器进程被创建之后，尽管开启了Mount namespace，但是在它执行 chroot（或者 pivot_root）之前，容器进程一直可以看到宿主机上的整个文件系统。而宿主机上的文件系统也自然包括了我们要使用的容器镜像。镜像的各个层保存在 /var/lib/docker/aufs/diff 目录下，在容器进程启动后，它的rootfs会被挂载在/var/lib/docker/aufs/mnt/目录中。所以，只需要在rootfs准备好之后，在执行chroot之前，把Volume指定的宿主机目录（比如/home目录），挂载到指定的容器目录（比如/test目录）在宿主机上对应的目录（即 /var/lib/docker/aufs/mnt/[可读写层 ID]/test）上，这个Volume的挂载工作就完成了。由于执行这个挂载操作时，“容器进程”已经创建了，也就是Mount namespace已经开启。所以，这个挂载事件只在这个容器里可见，在宿主机上是看不见这个挂载点的，这也就保证了容器的隔离性不会被Volume打破。

这里通过Linux的绑定挂载技术，允许将一个目录或者文件而不是整个设备，挂载到一个指定的目录上。这时在该挂载点上进行的任何操作，只是发生在被挂载的目录或者文件上，而原挂载点的内容则会被隐藏起来且不受影响。

### 临时目录

在没有显示声明宿主机目录时，如``$ docker run -v /test ...``，Docker会默认在宿主机上创建一个临时目录/var/lib/docker/volumes/[VOLUME_ID]/_data，然后把它挂载到容器的指定的目录上。

### 指定目录

Docker把宿主机指定的目录挂载到容器指定的目录上，如``$ docker run -v /home:/test ...``。