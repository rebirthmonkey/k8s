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

> 这些命令将会创建一个名为mysql的容器（通过`--name mysql`），并将mysql数据卷映射到容器内的/var/lib/mysql
> MYSQL_IP 需要通过`docker network inspect python-server`获取
> 若要在宿主机运行`mysql`工具，需要使用`sudo apt-get install mysql-client`安装
> `-e MYSQL_ROOT_PASSWORD=P@ssw0rd` 将MySQL的root密码以环境变量的形式传进了容器。容器初始化的时候会使用该变量初始化root密码

在mysql中，执行下面两条mysql语句，赋予root@localhost访问权限

```mysql
mysql> GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost';
mysql> FLUSH PRIVILEGES;
```

如果无法从宿主机访问docker容器（即`mysql -h MYSQL_IP -u root -p`无法运行），则需要进入容器终端执行mysql

```bash
[host] $ docker exec -it $MYSQL_CT_ID /bin/bash
[ct] $ mysql -u root -p
Passowrd:
[ct] > 
```

## Python Server

Build python-server Docker Image

```shell
cd docker
docker build -t python-server:0.1 .
docker image list # check the image
```

### Launch Python Server

```shell
docker container run --name python-server -d --net python-server -p 6666:8888 python-server:0.1 # use default env
docker container run --name python-server -d --net python-server -p 6666:8888 -e MYSQL_HOST=mysql python-server:0.1 # use new env
```

### Initialize MySQL DB

我们查看db1_tbl1.sql的内容，里面是一些SQL语句

```sql
# noinspection SqlNoDataSourceInspectionForFile
CREATE DATABASE db1;
USE db1;

CREATE TABLE IF NOT EXISTS `tbl1`(
   `tbl1_id` INT UNSIGNED AUTO_INCREMENT,
   `tbl1_title` VARCHAR(100) NOT NULL,
   `tbl1_author` VARCHAR(40) NOT NULL,
   `submission_date` DATE,
   PRIMARY KEY ( `tbl1_id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO tbl1 (tbl1_title, tbl1_author, submission_date) VALUES
    ("aaa", "111", '2001-05-06'),
    ("bbb", "222", '2002-05-06'),
    ("ccc", "333", '2003-05-06'),
    ("ddd", "444", '2004-05-06'),
    ("eee", "555", '2005-05-06'),
    ("fff", "666", '2006-05-06'),
    ("ggg", "777", '2007-05-06'),
    ("hhh", "888", '2008-05-06'),
    ("iii", "999", '2009-05-06'),
    ("jjj", "000", '2010-05-06');
```

```shell
mysql -h MYSQL_IP -u root -p < db1_tbl1.sql # init the db1 database of mysql
```

> 该步骤需要在宿主机执行，因db1_tbl1.sql文件不在容器内

check

```shell
curl localhost:6666
```
