# Django Messaging App - Kubernetes Deployment Makefile

.PHONY: help build deploy test clean status logs port-forward

# Default target
help:
	@echo "Django Messaging App - Kubernetes Deployment"
	@echo ""
	@echo "Available targets:"
	@echo "  build         Build Docker image"
	@echo "  deploy        Deploy to Kubernetes cluster"
	@echo "  test          Run deployment tests"
	@echo "  status        Show deployment status"
	@echo "  logs          Show application logs"
	@echo "  port-forward  Forward port 8000 to local machine"
	@echo "  scale         Scale deployment (use: make scale REPLICAS=5)"
	@echo "  clean         Remove deployment from cluster"
	@echo "  help          Show this help message"

# Build Docker image
build:
	@echo "Building Docker image..."
	cd .. && docker build -t messaging-app:latest .
	@echo "Image built successfully"

# Deploy to Kubernetes
deploy:
	@echo "Deploying to Kubernetes..."
	kubectl apply -f configmap.yaml
	kubectl apply -f secret.yaml
	kubectl apply -f deployment.yaml
	kubectl apply -f service.yaml
	@echo "Waiting for pods to be ready..."
	kubectl wait --for=condition=ready pod -l app=messaging-app --timeout=300s
	@echo "Deployment completed!"

# Test deployment
test:
	@echo "Running deployment tests..."
	./test-deployment.sh

# Show deployment status
status:
	@echo "Deployment Status:"
	@echo "=================="
	@kubectl get deployments -l app=messaging-app
	@echo ""
	@echo "Pods:"
	@echo "====="
	@kubectl get pods -l app=messaging-app
	@echo ""
	@echo "Services:"
	@echo "========="
	@kubectl get services -l app=messaging-app

# Show application logs
logs:
	kubectl logs -l app=messaging-app -f

# Forward port to local machine
port-forward:
	@echo "Forwarding port 8000 to localhost:8000"
	@echo "Visit: http://localhost:8000"
	@echo "Press Ctrl+C to stop"
	kubectl port-forward service/messaging-app-service 8000:8000

# Scale deployment
REPLICAS ?= 3
scale:
	kubectl scale deployment messaging-app-deployment --replicas=$(REPLICAS)
	@echo "Scaled to $(REPLICAS) replicas"

# Clean up deployment
clean:
	@echo "Removing deployment from cluster..."
	-kubectl delete -f deployment.yaml
	-kubectl delete -f service.yaml
	-kubectl delete -f configmap.yaml
	-kubectl delete -f secret.yaml
	@echo "Cleanup completed"

# Quick deployment (build + deploy)
quick-deploy: build deploy

# Full workflow (build + deploy + test)
full-deploy: build deploy test status
