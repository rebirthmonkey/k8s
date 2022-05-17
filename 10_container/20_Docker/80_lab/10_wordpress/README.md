# WordPress

In order to deploy a *wordpress* application, we should:

- create 1 network
- create 2 volumes
  - 1 for mysql
  - 1 for wordpress
- launch the *mysql* container
- launch the *wordpress* container

## Docker Deployment

Network Creation

```shell
docker network create wordpress
docker network list
```

Volume Creation

```shell
docker volume create mysql
docker volume create wordpress
docker volume list
```

WordPress and MySQL Image Download

```shell
docker image pull wordpress:4.9.6
docker image inspect wordpress:4.9.6
docker image pull mysql:5.7
docker image inspect mysql:5.7
```

Launch the Container MySQL

```shell
docker run --name wordpressdb -d --rm \ # name可以随便取
--net wordpress \ # 连接到wordpress网络
-v mysql:/var/lib/mysql \
-e MYSQL_ROOT_PASSWORD=P@ssw0rd \
-e MYSQL_DATABASE=wordpress \ # 必须是wordpress
mysql:5.7
```

Launch the Container Wordpress

```shell
docker run --name wordpress -d --rm \
--net wordpress \ # 连接到wordpress网络
-p 8090:80 \ # 端口映射，宿主机8090->容器80
-e WORDPRESS_DB_PASSWORD=P@ssw0rd \ # 这里要和前面保持一致
-e WORDPRESS_DB_HOST=wordpressdb \ # 这里要和前面保持一致
-v wordpress:/var/www/html \
wordpress:5.9.3
```

Check

```shell
curl http://localhost:8090 # through a browser
```
