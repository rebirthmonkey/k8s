# Installation
## Main Components
![Docker Main Components](figures/docker-architecture.png)

- Docker client: send commands
- Docker Daemon: server to handle requests
  - `/etc/systemd/system/multi-user.target.wants/docker.serivce` `-H tcp://0.0.0.0`: configuration to accept remote requests (no need to do)
  - `systemctl daemon-reload` and `systemctl restart docker.service`
  - `docker -H 192.168.88.8 info`: example (no need to do)
- Registry: host Docker images


## Auto-Install
- `curl https://get.docker.com/ | sh`
- `wget -qO- https://get.docker.com/ | sh`


## Debian APT Installation
```bash
sudo apt-get remove docker docker-engine docker.io
sudo apt-get remove docker-compose
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install docker-ce
```


## No-Root Configuration
- `sudo groupadd docker`
- `sudo usermod -aG docker $USER`
- logout and then login to take effect


## Chinese Docker Repo Mirrors
```bash
sudo vi /etc/docker/daemon.json
{
  "registry-mirrors": ["https://registry.docker-cn.com"]
}
systemctl daemon-reload
systemctl restart docker
```


## Test
- `dockeer --version`
- `docker info`
- `docker run hello-world`


## Troubleshooting
### Failed to start Docker Application Container Engine
Cannot load hosts in configuration json file when starting docker daemon
- `vim /lib/systemd/system/docker.service`
- `ExecStart=/usr/bin/dockerd`
- `# -H fd://`

## Ref
Official documentation for installation:
https://docs.docker.com/install/linux/docker-ce/ubuntu/

