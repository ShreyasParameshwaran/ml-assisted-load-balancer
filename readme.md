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

enabled ingress addon in minikube 

added nginx-ingress-controller using helm installation

created a minikube tunnel to assign external ip to nginx controller 

created a configMap of type ingress and applied to cluster

port forwarded localhost to nginx controller external ip using ``` kubectl port-forward service/ingress-app-ingress-nginx-controller 8080:80``` 

enabled service monitoring in nginx ingress controller so prometheus can scrape metrics from it

successfully created nodeapp through nginx tunnel
