FROM ubuntu:xenial

RUN apt update && \
    apt install -y nodejs-legacy

COPY . /data
WORKDIR /data

CMD ["node", "backend_server.js"]
