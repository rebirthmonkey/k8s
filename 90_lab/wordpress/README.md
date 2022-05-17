# WordPress Lab

## create pods

- create 1 mysql deployment
  - `kubectl apply -f mysql-deployment.yml`
- create 1 mysql service
  - `kubectl apply -f mysql-service.yml`
- create 1 wordpress deployment
  - `kubectl apply -f wordpress-deployment.yml`
- create 1 wordpress service
  - `kubectl apply -f wordpress-service.yml`
- create 1 ingress LB
  - `minikube addons enable ingress`: install ingress
  - `echo "$(minikube ip) ingress.minikube" | sudo tee -a /etc/hosts`: add host name to /etc/hosts
  - `kubectl apply -f wordpress-ingress.yml`: create ingress

## create 2 persistent volumes

  - `/var/lib/mysql` for MySQL deployment
    - `kubectl apply -f mysql-pv.yml`
    - `kubectl apply -f mysql-pvc.yml`: create `mysql-pvc`
    - `kubectl apply -f mysql-deployment2.yml`
    - `kubectl apply -f mysql-service.yml`
  - `/var/www/html` for Wordpress deployment
    - `kubectl apply -f wordpress-pv.yml`
    - `kubectl apply -f wordpress-pvc.yml`: create `wordpress-pvc`
    - `kubectl apply -f wordpress-deployment2.yml`
    - `kubectl apply -f wordpress-service.yml`
