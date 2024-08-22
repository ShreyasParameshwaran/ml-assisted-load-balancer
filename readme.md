## Prerequisites

Before running the cluster creation script, ensure you have the following installed:

- **Minikube**: [Install Minikube](https://minikube.sigs.k8s.io/docs/start/)
- **kubectl**: [Install kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- **gnome-terminal**: Ensure you have `gnome-terminal` installed. If using a different terminal emulator, adjust the script accordingly.

## Script Usage

1. **Use the Script**: Use the `setup_minikube.sh` script in the repository root folder:

2. **Make the Script Executable**:

    ```bash
    chmod +x setup_minikube.sh
    ```

3. **Run the Script**:

    ```bash
    ./setup_minikube.sh
    ```

4. Run minikube tunnel in a new terminal

    ```bash
    minikube tunnel
    ```

5. Run port-forward for Prometheus in a new terminal
    ```bash
    kubectl port-forward service/prometheus-kube-prometheus-prometheus 9090:9090 -n monitoring
    ```

6. Run port-forward for Ingress-NGINX in a new terminal
    ```bash
    kubectl port-forward service/ingress-app-ingress-nginx-controller 3000:80
    ```

7. Run port-forward for ML API service in a new terminal
    ```bash
    kubectl port-forward service/ml-api-service 5000:5000
    ```
8. Visit Localhost
    - http://localhost:3000 - Web App
    - http://localhost:9000 - Prometheus
    - http://localhost:5000/predict - ML API

# Content below is deprecated
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
