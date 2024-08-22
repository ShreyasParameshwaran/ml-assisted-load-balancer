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

# Run kubectl get all in a new terminal
echo "Running kubectl get all..."
open_new_terminal "kubectl get all"

echo "All commands have been executed."
