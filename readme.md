## PRE REQUISITES 
docker
minikube
kubectl
helm

first created a new docker image of simple hello world using node js
pushed above mentioned image to docker hub



steps to launch minikube use command ```minikube start```

created a kubernetes deployment yml and kubernetes service yml to specify ports 
created cluster
installed prometheus and grafana onto cluster using helm


linked grafana to prometheus using service url in the form of   ```http://<node-ip>:<node-port>```


exposed new service of prometheus server using command ```kubectl expose service prometheus-server --type=NodePort --target-port=9090 --name=prometheus-server-ext```

to get prometheus ui after launching k8, use command ```minikube service prometheus-server-ext```

exposed grafana to port 3000 using ``` kubectl expose service grafana --type=NodePort --target-port=3000 --name=grafana-ext```

to get grafana ui we use ```minikube service grafana-ext```

added addditional-scrape-configs file to add an extra end point in prometheus

mounted this on prometheus server yaml file using ```kubectl edit deployment prometheus-server```



