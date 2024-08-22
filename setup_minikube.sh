#!/bin/bash

# Function to open a new terminal and run a command
open_new_terminal() {
    local command="$1"
    gnome-terminal -- bash -c "$command; exec bash"
}

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
open_new_terminal "minikube tunnel"

# Run port-forward for Prometheus in a new terminal
echo "Starting port-forward for Prometheus..."
open_new_terminal "kubectl port-forward service/prometheus-kube-prometheus-prometheus 9090:9090 -n monitoring"

# Run port-forward for Ingress-NGINX in a new terminal
echo "Starting port-forward for Ingress-NGINX..."
open_new_terminal "kubectl port-forward service/ingress-app-ingress-nginx-controller 3000:80"

# Run port-forward for ML API service in a new terminal
echo "Starting port-forward for ML API service..."
open_new_terminal "kubectl port-forward service/ml-api-service 5000:5000"

# Run kubectl get all in a new terminal
echo "Running kubectl get all..."
open_new_terminal "kubectl get all"

echo "All commands have been executed."
