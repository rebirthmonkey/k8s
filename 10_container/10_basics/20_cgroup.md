# Cgroup

cgroup是Linux内核中的一项功能，它可以对进程进行分组，并在分组的基础上对进程组进行资源分配（如 CPU时间、系统内存、网络带宽等）。通过cgroup，系统管理员在分配、排序、拒绝、管理和监控系统资源等方面，可以对硬件资源进行精细化控制。cgroup的目的和namespace不一样，namespace是为了隔离进程之间的资源，而cgroup是为了对一组进程进行统一的资源监控和限制。

cgroup技术就是把系统中所有进程组织成一颗进程树，进程树都包含系统的所有进程，树的每个节点是一个进程组。cgroup中的资源被称为subsystem，进程树可以和一个或者多个subsystem系统资源关联。系统中可以有很多颗进程树，每棵树都和不同的subsystem关联，一个进程可以属于多颗树，即一个进程可以属于多个进程组，只是这些进程组和不同的subsystem关联。进程树的作用是将进程分组，而subsystem的作用是监控、调度或限制每个进程组的资源。目前Linux支持12种subsystem，比如限制CPU的使用时间、内存、统计CPU的使用情况等。也就是Linux里面最多可以建12棵进程树，每棵树关联一个subsystem，当然也可以只建一棵树，然后让这棵树关联所有的subsystem。

在CentOS 7系统中通过将cgroup层级系统与systemd单位树捆绑，可以把资源管理设置从进程级别移至应用程序级别。默认情况下，systemd会自动创建slice、scope和service单位的层级，来为cgroup树提供统一结构。如果我们将系统的资源看成一块馅饼，那么所有资源默认会被划分为 3 个cgroup：System、User和Machine，每一个cgroup都是一个slice，每个slice都可以有自己的子slice。

## 操作

- 列出所有cgroup的subsystem

```shell
$ lssubsys –m
```

> 可能需要安装cgroup-tools
>
>```shell
># debian/ubuntu
>sudo apt-get install cgroup-tools
>```

输出：

```text
cpuset /sys/fs/cgroup/cpuset cpu,cpuacct /sys/fs/cgroup/cpu,cpuacct memory /sys/fs/cgroup/memory devices /sys/fs/cgroup/devices
freezer /sys/fs/cgroup/freezer
net_cls /sys/fs/cgroup/net_cls
blkio /sys/fs/cgroup/blkio
hugetlb /sys/fs/cgroup/hugetlb
```

- 限制CPU

```bash
$ ls /sys/fs/cgroup/cpu/mytest
ls: cannot access /sys/fs/cgroup/cpu/mytest: No such file or directory

$ cgcreate -g cpu:mytest
$ ls /sys/fs/cgroup/cpu/mytest 
cpu.cfs_quota_us cpu.cfs_period_us tasks
$ while :; do :; done &
[2] 1759

$ top -p 1759
PID USER PR NI VIRT RES SHR S %CPU %MEM TIME+ COMMAND
1759 root 20 0 10956 1064 376 R 100.0 0.0 0:28.85 bash

$ cat /sys/fs/cgroup/cpu/mytest/cpu.cfs_period_us
100000

$ cat /sys/fs/cgroup/cpu/mytest/cpu.cfs_quota_us
-1

$ cat /sys/fs/cgroup/cpu/mytest/tasks
$ echo 30000 > /sys/fs/cgroup/cpu/mytest/cpu.cfs_quota_us 
$ cgclassify -g cpu:mytest 1759
$ cat /sys/fs/cgroup/cpu/mytest/cpu.cfs_quota_us
30000

$ cat /sys/fs/cgroup/cpu/mytest/tasks
1759

$ top –p 1759
PID USER PR NI VIRT RES SHR S %CPU %MEM TIME+ COMMAND 
1759 root 20 0 10956 1064 376 R 30.0 0.0 5:40.76 bash
```

> `echo 30000 > /sys/fs/cgroup/cpu/mytest/cpu.cfs_quota_us`这条命令可能会遇到权限问题，可以用 `echo 30000 | sudo tee /sys/fs/cgroup/cpu/test/cpu.cfs_quota_us`替代

> 可以用`while :; do :; done & echo $! > test.pid && cat test.pid` 将进程的PID保存在`test.pid`中，然后用`$(cat test.pid)`在命令中调用

- 限制磁盘I/O

```bash
$ dd if=/dev/sda1 of=/dev/null
$ iotop # iotop查看
TID PRIO USER DISK READ DISK WRITE SWAPIN IO> COMMAND
8128 be/4 root 55.74 M/s 0.00 B/s 0.00 % 85.65 % dd if=/de~=/dev/null...
$ mkdir /sys/fs/cgroup/blkio/mytest
$ echo '8:0 1048576' > /sys/fs/cgroup/blkio/mytest/blkio.throttle.read_bps_device 
$ echo 8128 > /sys/fs/cgroup/blkio/mytest/tasks
TID PRIO USER DISK READ DISK WRITE SWAPIN IO> COMMAND
8128 be/4 root 973.20 K/s 0.00 B/s 0.00 % 94.41 % dd if=/de~=/dev/null...
```

> `/dev/sda1`是需要读取的设备名称，必须存在（不同平台可能不同）

> `echo 8128 > /sys/fs/cgroup/blkio/mytest/tasks` 中，8128是进程的PID，需要修改

> `echo '8:0 1048576' > /sys/fs/cgroup/blkio/mytest/blkio.throttle.read_bps_device` 中，`8:0`对应主设备号和副设备号，可以通过`ls -l /dev/sda1`查看，`1048576`意味着速度被限制在1MiB/s

> 可能需要安装`iotop`

```shell
$ sudo apt-get install iotop
```

实验结束，删除cgroup，结束进程

```shell
$ sudo cgdelete cpu:mytest
$ sudo cgdelete blkio:mytest
$ kill -9 1759
```
