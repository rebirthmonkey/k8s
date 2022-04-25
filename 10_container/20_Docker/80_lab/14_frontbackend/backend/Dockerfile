FROM ubuntu:focal

RUN apt update && \
    apt install -y nodejs

COPY . /data
WORKDIR /data

CMD ["node", "backend_server.js"]
