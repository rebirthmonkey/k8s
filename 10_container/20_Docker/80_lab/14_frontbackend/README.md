# Frontend & Backend Web

## Dockerfile 解释

### Backend

```Dockerfile
# 基于ubuntu
FROM ubuntu:focal

# 安装nodejs
RUN apt update && \
    apt install -y nodejs

# 拷贝input.txt，backend_server.js到容器内
COPY . /data

# 设置/data目录为工作目录
WORKDIR /data

# 使用node运行backend_server.js
CMD ["node", "backend_server.js"]

```

### Frontend

大同小异

### 操作

### Build Images

```shell
docker image build -t backend backend
docker image build -t frontend frontend
```

### Create Network

```shell
docker network create frontbackend
```

### Launch Containers

```shell
docker container run --name backend -d --net=frontbackend backend
docker container run --name frontend -d --net=frontbackend -p 6666:8888 frontend
```

### Check

```shell
curl localhost:6666 # type twice
```

### 修改input.txt，模拟后端行为

modify the file `backend:/data/input.txt`, check the server again

> 我们需要修改的是backend容器内的`/data/input.txt`，由于容器内的`input.txt`在编译镜像中通过`COPY`命令进行了拷贝，因此和本地的input.txt文件相互独立。因此，我们需要进入容器进行修改，例如：

    ```shell
    [host] $ docker exec -it backend /bin/bash
    [ct] $ echo "xxx" > /data/input.txt
    ```

    其中`xxx`为自定义的文本内容

```shell
curl localhost:6666 #  type twice to see the update
```

## Q: 为什么需要Check两次server？

A: 这是因为在`frontend_server.js`中，向后端发起的请求是异步的。因此，每当用户curl前端，前端首先向后端发起一个请求以获取一个更新后的input.txt，并在回调函数中将其保存在`body_data`变量中。随后，前端立即返回一个`body_data`当前的值，此时请求尚未完成，因此前端返回一个较旧的数据
