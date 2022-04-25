FROM ubuntu:focal

RUN apt-get update && \
    apt-get -y install python3 python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install flask configparser pymysql

ENV MYSQL_HOST=localhost
ENV MYSQL_USER=root
ENV MYSQL_PASSWORD=P@ssw0rd
ENV MYSQL_DATABASE=db1

ADD . /data
WORKDIR /data

EXPOSE 8888

ENTRYPOINT python3 server.py --mysql_host $MYSQL_HOST --mysql_user $MYSQL_USER --mysql_password $MYSQL_PASSWORD --mysql_database $MYSQL_DATABASE