# Nginx Ingress Controller Principle
## Nginx Conf
### HTTP
- server: listen to a domain name
- upstream: bind a server to a backend service

### HTTPS
In the server, listens not only to the 80 port, but also to the 443 port
- `/etc/ingress-controller/ssl/default-fake-certificate.pem`: server.key + server.crt

