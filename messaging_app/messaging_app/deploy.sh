#!/bin/bash

# Django Messaging App - Kubernetes Deployment Script
# This script deploys the Django messaging app to Kubernetes

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if kubectl is available
check_kubectl() {
    if ! command -v kubectl &> /dev/null; then
        print_error "kubectl is not installed or not in PATH"
        exit 1
    fi
    print_success "kubectl is available"
}

# Function to check if cluster is accessible
check_cluster() {
    print_status "Checking Kubernetes cluster connectivity..."
    if kubectl cluster-info &> /dev/null; then
        print_success "Kubernetes cluster is accessible"
    else
        print_error "Cannot connect to Kubernetes cluster"
        print_status "Make sure your cluster is running and kubectl is configured"
        exit 1
    fi
}

# Function to build Docker image if it doesn't exist
build_or_load_image() {
    print_status "Checking for Docker image..."
    
    # Check if image exists locally
    if docker images messaging-app:latest --format "table {{.Repository}}" | grep -q messaging-app; then
        print_success "Docker image 'messaging-app:latest' found locally"
    else
        print_warning "Docker image 'messaging-app:latest' not found locally"
        print_status "Building Docker image..."
        
        # Go to parent directory where Dockerfile is located
        if [ -f "../Dockerfile" ]; then
            cd ..
            docker build -t messaging-app:latest .
            cd messaging_app
            print_success "Docker image built successfully"
        else
            print_error "Dockerfile not found. Please build the image manually:"
            echo "  docker build -t messaging-app:latest ."
            exit 1
        fi
    fi
    
    # Load image into minikube if using minikube
    if kubectl config current-context 2>/dev/null | grep -q minikube; then
        print_status "Loading image into Minikube..."
        minikube image load messaging-app:latest
        print_success "Image loaded into Minikube"
    fi
}

# Function to apply Kubernetes manifests
apply_manifests() {
    print_status "Applying Kubernetes manifests..."
    
    # Apply in order: ConfigMap, Secret, Deployment, Service
    if [ -f "configmap.yaml" ]; then
        kubectl apply -f configmap.yaml
        print_success "ConfigMap applied"
    fi
    
    if [ -f "secret.yaml" ]; then
        kubectl apply -f secret.yaml
        print_success "Secret applied"
    fi
    
    if [ -f "deployment.yaml" ]; then
        kubectl apply -f deployment.yaml
        print_success "Deployment applied"
    else
        print_error "deployment.yaml not found"
        exit 1
    fi
    
    if [ -f "service.yaml" ]; then
        kubectl apply -f service.yaml
        print_success "Service applied"
    fi
}

# Function to wait for pods to be ready
wait_for_pods() {
    print_status "Waiting for pods to be ready..."
    kubectl wait --for=condition=ready pod -l app=messaging-app --timeout=300s
    print_success "Pods are ready"
}

# Function to verify deployment
verify_deployment() {
    print_status "Verifying deployment..."
    
    echo -e "\n${BLUE}Deployments:${NC}"
    kubectl get deployments -l app=messaging-app
    
    echo -e "\n${BLUE}Pods:${NC}"
    kubectl get pods -l app=messaging-app
    
    echo -e "\n${BLUE}Services:${NC}"
    kubectl get services -l app=messaging-app
    
    echo -e "\n${BLUE}Pod logs (last 10 lines):${NC}"
    kubectl logs -l app=messaging-app --tail=10
}

# Function to provide post-deployment information
show_access_info() {
    print_success "Deployment completed successfully!"
    
    echo -e "\n${GREEN}Access Information:${NC}"
    echo -e "${BLUE}To access the application:${NC}"
    echo "  kubectl port-forward service/messaging-app-service 8000:8000"
    echo "  Then visit: http://localhost:8000"
    
    echo -e "\n${BLUE}Useful commands:${NC}"
    echo "  kubectl get pods -l app=messaging-app     # Check pod status"
    echo "  kubectl logs -l app=messaging-app -f      # View logs"
    echo "  kubectl describe pod <pod-name>           # Pod details"
    echo "  kubectl scale deployment messaging-app-deployment --replicas=5  # Scale app"
    
    echo -e "\n${BLUE}To remove the deployment:${NC}"
    echo "  kubectl delete -f deployment.yaml"
    echo "  kubectl delete -f service.yaml"
    echo "  kubectl delete configmap messaging-app-config"
    echo "  kubectl delete secret messaging-app-secret"
}

# Main function
main() {
    echo -e "${GREEN}================================================${NC}"
    echo -e "${GREEN}  Django Messaging App - Kubernetes Deployment  ${NC}"
    echo -e "${GREEN}================================================${NC}"
    echo ""
    
    # Pre-flight checks
    check_kubectl
    check_cluster
    
    # Build or load Docker image
    build_or_load_image
    
    # Deploy to Kubernetes
    apply_manifests
    
    # Wait for pods to be ready
    wait_for_pods
    
    # Verify deployment
    verify_deployment
    
    # Show access information
    show_access_info
}

# Run main function
main "$@"
