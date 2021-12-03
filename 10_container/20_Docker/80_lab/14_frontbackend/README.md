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
# modify the `backend/input.txt` file
curl localhost:6666 #  type twice to see the update
```