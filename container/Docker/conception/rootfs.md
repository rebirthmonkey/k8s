# rootfs

## Introduction

Union File System可以将多个不同位置的目录联合挂载(union mount)到同一个目录下。Docker利用这种联合挂载的能力，将容器镜像里的多层内容呈现为统一的rootfs。Rootfs打包了整个操作系统的文件和目录，是应用运行所需要的最完整的“依赖库”。



## Exercises

### aufs

- 上层覆盖下层

```bash
$ grep aufs /proc/filesystems
nodev aufs
[root@TENCENT64 /data/kendywang/test]$ tree .
|-- aufs-mnt
|-- container-layer
|-- image-layer-high
| |-- image-layer-high.txt
| `-- x.txt
`-- image-layer-low
|-- image-layer-low.txt `-- x.txt
$ mount -t aufs -o dirs=./container-layer:./image-layer-high:./image-layer-low none ./aufs-mnt
$ mount -t aufs
none on /data/kendywang/test/aufs-mnt type aufs (rw,relatime,si=e7b69dd2200efd9f)
$ cat /sys/fs/aufs/si_e7b69dd2200efd9f/*
/data/kendywang/test/container-layer=rw /data/kendywang/test/image-layer-high=ro /data/kendywang/test/image-layer-low=ro
$ ls /data/kendywang/test/aufs-mnt
image-layer-high.txt image-layer-low.txt x.txt
$ cat /data/kendywang/test/aufs-mnt/x.txt
x.txt from image layer high.
```

- 新增读写层

```bash
$ echo "I am container layer." >> /data/kendywang/test/aufs-mnt/container- layer.txt
$ cat /data/kendywang/test/aufs-mnt/container-layer.txt
I am container layer.
$ cat /data/kendywang/test/container-layer/container-layer.txt
I am container layer.
```

- 写时拷贝

```bash
#修改文件
$ echo "modify txt" >> /data/kendywang/test/aufs-mnt/image-layer-low.txt $ cat /data/kendywang/test/aufs-mnt/image-layer-low.txt
I am image layer low.
modify txt
#image-layer-low目录文件没有改变
$ cat /data/kendywang/test/image-layer-low/image-layer-low.txt
I am image layer low.
#被修改文件copy到了container-layer
$ cat /data/kendywang/test/container-layer/image-layer-low.txt
I am image layer low. modify txt
```

- 通过whiteout删除文件

```bash
$ cat /data/kendywang/test/aufs-mnt/image-layer-high.txt
I am image layer high.
$ rm /data/kendywang/test/aufs-mnt/image-layer-high.txt $ cat /data/kendywang/test/aufs-mnt/image-layer-hight.txt cat: image-layer-hight.txt: No such file or directory
$ cat /data/kendywang/test/image-layer-high/image-layer-high.txt
I am image layer high.
$ ls -a /data/kendywang/test/container-layer/.wh.image-layer-high.txt
/data/kendywang/test/container-layer/.wh.image-layer-high.txt
```

- 总结

![image-20200202121527484](figures/image-20200202121527484.png)













