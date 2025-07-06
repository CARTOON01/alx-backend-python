#!/bin/bash

# Quick Start Script for Django Messaging App Kubernetes Deployment
# This script does everything needed to get the app running on Kubernetes

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo -e "${GREEN}============================================${NC}"
    echo -e "${GREEN}  Django Messaging App - Quick Start       ${NC}"
    echo -e "${GREEN}============================================${NC}"
    echo ""
}

print_status() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
check_directory() {
    if [ ! -f "deployment.yaml" ]; then
        print_error "Please run this script from the messaging_app directory"
        exit 1
    fi
}

# Step 1: Set up Kubernetes cluster
setup_cluster() {
    print_status "Setting up Kubernetes cluster..."
    
    if command -v minikube &> /dev/null; then
        if ! minikube status &> /dev/null; then
            print_status "Starting Minikube cluster..."
            ./kurbeScript
        else
            print_success "Minikube cluster is already running"
        fi
    else
        print_error "Minikube not found. Please install Minikube or ensure kubectl is configured for your cluster"
        exit 1
    fi
}

# Step 2: Build Docker image
build_image() {
    print_status "Building Docker image..."
    cd ..
    docker build -t messaging-app:latest .
    cd messaging_app
    print_success "Docker image built"
    
    # Load into Minikube if applicable
    if minikube status &> /dev/null; then
        print_status "Loading image into Minikube..."
        minikube image load messaging-app:latest
        print_success "Image loaded into Minikube"
    fi
}

# Step 3: Deploy to Kubernetes
deploy_app() {
    print_status "Deploying application to Kubernetes..."
    
    kubectl apply -f configmap.yaml
    kubectl apply -f secret.yaml
    kubectl apply -f deployment.yaml
    kubectl apply -f service.yaml
    
    print_success "Kubernetes manifests applied"
    
    print_status "Waiting for pods to be ready..."
    kubectl wait --for=condition=ready pod -l app=messaging-app --timeout=300s
    print_success "Pods are ready"
}

# Step 4: Test deployment
test_deployment() {
    print_status "Testing deployment..."
    ./test-deployment.sh
}

# Step 5: Show access instructions
show_access() {
    print_success "Deployment completed successfully!"
    echo ""
    echo -e "${GREEN}Your Django Messaging App is now running on Kubernetes!${NC}"
    echo ""
    echo -e "${BLUE}To access the application:${NC}"
    echo "1. Run: kubectl port-forward service/messaging-app-service 8000:8000"
    echo "2. Visit: http://localhost:8000"
    echo ""
    echo -e "${BLUE}Quick commands:${NC}"
    echo "• Status: kubectl get pods -l app=messaging-app"
    echo "• Logs:   kubectl logs -l app=messaging-app -f"
    echo "• Scale:  kubectl scale deployment messaging-app-deployment --replicas=5"
    echo ""
    echo -e "${BLUE}Or use the Makefile:${NC}"
    echo "• make status"
    echo "• make logs"
    echo "• make port-forward"
    echo "• make scale REPLICAS=5"
}

# Main execution
main() {
    print_header
    
    check_directory
    setup_cluster
    build_image
    deploy_app
    test_deployment
    show_access
}

main "$@"
