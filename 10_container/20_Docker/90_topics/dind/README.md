# DinD
A detailed description can be found [here](http://blog.teracy.com/2017/09/11/how-to-use-docker-in-docker-dind-and-docker-outside-of-docker-dood-for-local-ci-testing/)

## Build & Run Container
- `cd dind/`
- `docker build -t centos:7-dind -f Dockerfile .`
- `docker run --privileged -d --name dind centos:7-dind`
