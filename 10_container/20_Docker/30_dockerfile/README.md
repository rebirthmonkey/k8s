# Dockerfile

Dockerfile specifies all the configurations to build an image.

## Syntax

- `FROM`: base image，设置基础镜像为 Debian
- `LABEL`: 来给 image 添加 metadata，是 key-value 键值对的形式。

  - `LABEL version="1.0"`

  - `docker image inspect --format='' myimage`：查看 label
- `ENV`: define environment variables to be used by *RUN*, *ENTRYPOINT*, *CMD*

  - `ENV MY_VERSION="1.3"`
- `USER`: execute the commands with which user
- `WORKDIR`: switch path inside the container
  - `WORKDIR /path/to/workdir`
- `COPY/ADD`: copy files from the host to the container
  - `COPY index.html /var/www/html/index.html`
  - `COPY ["index.html", "/var/www/html/index.html"]`
  - `ADD`: can unzip tar, zip, taz files，将软件包解压到/xxx/目录下
- `VOLUME`: create default mount points，设置 volume 到目录 /xxx/ 下
  - `VOLUME ["/etc/mysql/mysql.conf.d", "/var/lib/mysql", "/var/log/mysql"]`
- `EXPOSE`: export a TCP/UDP port on the container
  - -p：发布一个或多个端口
  - -P：发布全部端口，并映射到高位端口
- `RUN`: 构建镜像时会执行的命令。effectuate actions as ‘install packages’, 'modify configuration', 'create links and directories', 'create users and groups'.

  - `RUN apt-get install -y mypackage=$MY_VERSION`
  - `RUN ["/bin/bash", "-c", "echo hello"]`
- `CMD`: 启动容器时会执行的命令。command to be run when launch the container。CMD 与 RUN不同，RUN 是在 build 镜像过程中执行的命令，而 CMD 在 build 时不会执行任何命令，而是在容器启动时（镜像创建的容器）执行。

  - if there are multiple CMD, only the last will be run
- `ENTRYPOINT`: docker run 命令的参数会被添加到 ENTRYPOINT 中的所有元素之后，并覆盖 CMD 命令。如果不填 ENTRYPOINT，默认用`/bin/bash -c`代替

  - always run even if add another NEW_CMD

  - `docker container run NEW_CMD`: NEW_CMD will be added as parameters to ENTRYPOINT, and replace CMD

  - `ENTRYPOINT ["top", "-b"]`
- `ONBUILD`：会在镜像中添加一个 trigger，这个 trigger 会在镜像作为 base 时触发。
- STOPSIGNAL：设置 system call signal，发送到容器退出。
- `HEALTHCHECK`：用来告诉 Docker 怎样测试本容器是否还在工作。
- `SHELL`: use which shell to execute commands.

## 最佳实践

- 建议所有的 Dockerfile 指令大写，这样做可以很好地跟在镜像内执行的指令区分开来。
- 在选择基础镜像时，尽量选择官方的镜像，并在满足要求的情况下，尽量选择体积小的镜像。目前，Linux 镜像大小有以下关系：busybox < debian < centos <  ubuntu。最好确保同一个项目中使用一个统一的基础镜像。如无特殊需求，可以选择使用 debian:jessie 或 alpine。
- 在构建镜像时，删除不需要的文件，只安装需要的文件，保持镜像干净、轻量。
- 使用更少的层，把相关的内容放到一个层，并使用换行符进行分割。这样可以进一步减小镜像的体积，也方便查看镜像历史。
- 不要在 Dockerfile 中修改文件的权限。因为如果修改文件的权限，Docker 在构建时会重新复制一份，这会导致镜像体积越来越大。
- 给镜像打上标签，标签可以帮助你理解镜像的功能，例如：docker build  -t="nginx:3.0-onbuild"。
- FROM 指令应该包含 tag，例如使用 FROM debian:jessie，而不是FROM debian。
- 充分利用缓存。Docker 构建引擎会顺序执行 Dockerfile  中的指令，而且一旦缓存失效，后续命令将不能使用缓存。为了有效地利用缓存，需要尽量将所有的 Dockerfile 文件中相同的部分都放在前面，而将不同的部分放在后面。
- 优先使用 COPY 而非 ADD 指令。和 ADD 相比，COPY 功能简单，而且也够用。ADD 可变的行为会导致该指令的行为不清晰，不利于后期维护和理解。
- 推荐将 CMD 和 ENTRYPOINT 指令结合使用，使用 execl 格式的 ENTRYPOINT 指令设置固定的默认命令和参数，然后使用 CMD 指令设置可变的参数。
- 尽量使用 Dockerfile 共享镜像。通过共享 Dockerfile，可以使开发者明确知道 Docker 镜像的构建过程，并且可以将 Dockerfile 文件加入版本控制，跟踪起来。
- 使用 .dockerignore 忽略构建镜像时非必需的文件。忽略无用的文件，可以提高构建速度。
- 使用多阶段构建。多阶段构建可以大幅减小最终镜像的体积。例如，COPY 指令中可能包含一些安装包，安装完成之后这些内容就废弃掉。

## Lab

### Build Image

- `docker image build` create a new image using the instructions in the Dockerfile
  - `docker image build -t apache2-demo:v1 .`: `-t` stands for tag/name
  - `docker image build -t apache2-demo:v1 -f DockerfileXXX .`: `-f` use a Dockerfile with an arbitrary name
- `docker image history apache2-demo`: show image build history

### Shell Env

```shell
docker build -t img1 -f Dockerfile-env . # create the image
docker run --name ct1 --rm img1 # see the default msg in default file /tmp/xxx.log
docker run --name ct2 --rm -e MSG=111 img1 # see the new msg
```

### Python Argparse Env

```shell
docker build -t img1 -f Dockerfile-env-python . # create the image
docker run --name ct1 --rm img1 # see the default msg
docker run --name ct2 --rm -e MSG1=aaa -e MSG2=bbb img1 # see the new msgs
```

### Same Image for Different Scripts

```shell
docker build -t img1 -f Dockerfile-env-python2 . # create the image
docker run --name ct2 --rm -v $(pwd):/workspace img1 # launch the default script
docker run --name ct2 --rm -v $(pwd):/workspace -e APP=/workspace/app2.py img1 # launch the new script
```

### Apache2 Web Server

- write a Dockerfile to create an image with packages php, apache (apache2, libapache2-mod-php)
- add a index.php file with: `<?php phpinfo() ?>`

See the [Dockerfile](Dockerfile) as the answer

```shell
docker image build -t apache2-demo .
docker run -d -p 8885:80 apache2-demo
http://localhost:8885/index.php # test NAT access through browser
```

> 安装镜像时可能会出现要求输入时区的情况，导致安装失败。需要在Dockerfile中添加`RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime`来设定当前时区为上海

## Ref

1. [Dockerfile文件万字全面解析](https://www.toutiao.com/i6865085292726977035/?tt_from=weixin&utm_campaign=client_share&wxshare_count=1&timestamp=1598448076&app=news_article&utm_source=weixin&utm_medium=toutiao_ios&use_new_style=1&req_id=202008262121160100180820431714AAB2&group_id=6865085292726977035)
