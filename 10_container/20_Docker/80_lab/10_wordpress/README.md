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
docker run --name wordpressdb -d --rm \
--net wordpress \
-v mysql:/var/lib/mysql \
-e MYSQL_ROOT_PASSWORD=P@ssw0rd \
-e MYSQL_DATABASE=wordpress \
mysql:5.7
```

Launch the Container Wordpress

```shell
docker run --name wordpress -d --rm \
--net wordpress -p 8090:80 \
-e WORDPRESS_DB_PASSWORD=P@ssw0rd -v wordpress:/var/www/html \
wordpress:4.9.6
```

Check

```shell
curl http://localhost:8090 # through a browser
```
