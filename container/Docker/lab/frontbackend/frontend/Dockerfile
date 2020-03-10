FROM ubuntu:xenial

RUN apt update && \
    apt install -y nodejs-legacy

COPY . /data
WORKDIR /data

EXPOSE 6666

CMD ["node", "frontend_server.js"]