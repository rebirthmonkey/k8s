FROM ubuntu:focal

RUN apt update && \
    apt install -y nodejs

COPY . /data
WORKDIR /data

EXPOSE 6666

CMD ["node", "frontend_server.js"]