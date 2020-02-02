# Configuration

## Image
- `/etc/docker/daemon.json`：set default image register (no need to do)

        {
          "registry-mirrors": ["https://10.123.97.147"],  
          "max-concurrent-downloads": 6,
          "insecure-registries" : ["docker-registry.xxx.com"] 
        }