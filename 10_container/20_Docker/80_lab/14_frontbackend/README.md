# Frontend & Backend Web

Build Images

```shell
docker image build -t backend backend
docker image build -t frontend frontend
```

Create Network

```shell
docker network create frontbackend
```

Launch Containers

```shell
docker container run --name backend -d --net=frontbackend backend
docker container run --name frontend -d --net=frontbackend -p 6666:8888 frontend
```

Check

```shell
curl localhost:6666 # type twice
```

modify the file `backend:/data/input.txt`, check the server again

```shell
curl localhost:6666 #  type twice to see the update
```

## Q: 为什么需要Check两次server？

A: 这是因为在`frontend_server.js`中，向后端发起的请求是异步的。因此，每当用户curl前端，前端首先向后端发起一个请求以获取一个更新后的input.txt，并在回调函数中将其保存在`body_data`变量中。随后，前端立即返回一个`body_data`当前的值，此时请求尚未完成，因此前端返回一个较旧的数据.wo
