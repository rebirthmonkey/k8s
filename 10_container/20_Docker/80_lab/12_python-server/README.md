# Python Web Server

## mysql

```shell
$ docker network create python-server # create a backend network
$ docker volume create mysql # create a volume
$ docker image pull mysql:5.7 
$ docker container run --name mysql -d --net python-server -v mysql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=P@ssw0rd  mysql:5.7
$ mysql -h MYSQL_IP -u root -p # test the access to the mysql server
Password: 
```

> MYSQL_IP 需要通过`docker network inspect python-server`获取
> 若要在宿主机运行`mysql`工具，需要使用`sudo apt-get install mysql-client`安装

在mysql终端中，执行下面两条mysql语句，赋予root@localhost访问权限

```mysql
GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
```

## Python Server

Build python-server Docker Image

```shell
cd docker
docker build -t python-server:0.1 .
docker image list # check the image
```

Launch Python Server

```shell
docker container run --name python-server -d --net python-server -p 6666:8888 python-server:0.1 # use default env
docker container run --name python-server -d --net python-server -p 6666:8888 -e MYSQL_HOST=mysql python-server:0.1 # use new env
```

Initialize MySQL DB

```shell
mysql -h MYSQL_IP -u root -p < db1_tbl1.sql # init the db1 database of mysql
```

check

```shell
curl localhost:6666
```
