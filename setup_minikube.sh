#!/bin/bash

# Start Minikube
echo "Starting Minikube..."
minikube start

# Change to the exports directory
cd exports || { echo "Directory 'exports' not found!"; exit 1; }

# Apply all YAML files in the exports directory
echo "Applying YAML files..."
find . -name '*.yaml' -exec kubectl apply -f {} \;

# Run minikube tunnel in a new terminal
echo "Starting minikube tunnel..."
gnome-terminal -- bash -c "minikube tunnel"

# Run port-forward for Prometheus in a new terminal
echo "Starting port-forward for Prometheus..."
gnome-terminal -- bash -c "kubectl port-forward service/prometheus-kube-prometheus-prometheus 9090:9090 -n monitoring"

# Run port-forward for Ingress-NGINX in a new terminal
echo "Starting port-forward for Ingress-NGINX..."
gnome-terminal -- bash -c "kubectl port-forward service/ingress-app-ingress-nginx-controller 3000:80"

# Run port-forward for ML API service in a new terminal
echo "Starting port-forward for ML API service..."
gnome-terminal -- bash -c "kubectl port-forward service/ml-api-service 5000:5000"

# Run kubectl get all in a new terminal
echo "Running kubectl get all..."
gnome-terminal -- bash -c "kubectl get all"

echo "All commands have been executed."
