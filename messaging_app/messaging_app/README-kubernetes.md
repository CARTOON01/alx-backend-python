# Django Messaging App - Kubernetes Deployment Guide

This directory contains Kubernetes deployment configurations for the Django Messaging App.

## Files Included

- `deployment.yaml` - Main deployment configuration with Service, ConfigMap, and Secret
- `service.yaml` - Standalone service configuration (ClusterIP) 
- `configmap.yaml` - Application configuration
- `secret.yaml` - Sensitive configuration data
- `deploy.sh` - Automated deployment script
- `test-deployment.sh` - Deployment verification script
- `Makefile` - Convenient deployment commands

## Quick Start

### Prerequisites

1. **Kubernetes cluster running** (use `./kurbeScript` to set up local cluster)
2. **kubectl configured** to communicate with your cluster
3. **Docker installed** for building images

### Option 1: Using the Deployment Script (Recommended)

```bash
# Run the automated deployment script
./deploy.sh
```

### Option 2: Using Makefile

```bash
# See available commands
make help

# Build and deploy
make build deploy

# Or do everything at once
make full-deploy
```

### Option 3: Manual Deployment

```bash
# Build Docker image
cd .. && docker build -t messaging-app:latest .

# If using Minikube, load the image
minikube image load messaging-app:latest

# Apply Kubernetes manifests
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# Wait for pods to be ready
kubectl wait --for=condition=ready pod -l app=messaging-app --timeout=300s
```

## Verification

### Check Deployment Status

```bash
# Check all resources
kubectl get deployments,pods,services -l app=messaging-app

# Or use the test script
./test-deployment.sh

# Or use make
make status
```

### View Application Logs

```bash
# View logs
kubectl logs -l app=messaging-app

# Follow logs
kubectl logs -l app=messaging-app -f

# Or use make
make logs
```

### Access the Application

```bash
# Port forward to local machine
kubectl port-forward service/messaging-app-service 8000:8000

# Or use make
make port-forward
```

Then visit: http://localhost:8000

## Configuration

### Environment Variables

The deployment uses the following environment variables:

- `DJANGO_SETTINGS_MODULE`: Django settings module (from ConfigMap)
- `SECRET_KEY`: Django secret key (from Secret)
- `DEBUG`: Debug mode (from ConfigMap, set to False)
- `ALLOWED_HOSTS`: Allowed host names (from ConfigMap)

### Resources

Each pod is configured with:
- **Requests**: 256Mi memory, 250m CPU
- **Limits**: 512Mi memory, 500m CPU

### Health Checks

- **Liveness Probe**: HTTP GET /api/ (starts after 30s, checks every 10s)
- **Readiness Probe**: HTTP GET /api/ (starts after 5s, checks every 5s)

## Scaling

Scale the deployment:
```bash
kubectl scale deployment messaging-app-deployment --replicas=5

# Or use make
make scale REPLICAS=5
```

## Advanced Operations

### Update the Application

```bash
# Build new image
docker build -t messaging-app:latest .

# If using Minikube, reload image
minikube image load messaging-app:latest

# Restart deployment to use new image
kubectl rollout restart deployment messaging-app-deployment
```

### View Detailed Information

```bash
# Describe deployment
kubectl describe deployment messaging-app-deployment

# Describe service
kubectl describe service messaging-app-service

# Get events
kubectl get events --sort-by=.metadata.creationTimestamp
```

### Configuration Changes

To update configuration:

1. Edit `configmap.yaml` or `secret.yaml`
2. Apply changes: `kubectl apply -f configmap.yaml`
3. Restart deployment: `kubectl rollout restart deployment messaging-app-deployment`

## Troubleshooting

### Common Issues

1. **ImagePullBackOff:**
   ```bash
   # For Minikube, load image locally
   minikube image load messaging-app:latest
   
   # Check if image exists
   docker images messaging-app:latest
   ```

2. **CrashLoopBackOff:**
   ```bash
   # Check logs for errors
   kubectl logs -l app=messaging-app
   
   # Check pod details
   kubectl describe pod <pod-name>
   ```

3. **Service not accessible:**
   ```bash
   # Check service endpoints
   kubectl get endpoints messaging-app-service
   
   # Verify service configuration
   kubectl describe service messaging-app-service
   ```

### Debug Commands

```bash
# Get pod shell access
kubectl exec -it <pod-name> -- /bin/bash

# Check pod environment variables
kubectl exec <pod-name> -- env

# Check if application is responding internally
kubectl exec <pod-name> -- curl http://localhost:8000/api/
```

## Cleanup

Remove the deployment:
```bash
# Using make
make clean

# Or manually
kubectl delete -f deployment.yaml
kubectl delete -f service.yaml
kubectl delete -f configmap.yaml
kubectl delete -f secret.yaml
```

## Production Considerations

For production deployment, consider:

1. **Use proper secrets management** (e.g., external secret operators)
2. **Configure persistent volumes** for database storage
3. **Set up ingress controller** for external access
4. **Configure resource quotas** and limits
5. **Set up horizontal pod autoscaling** (HPA)
6. **Use namespaces** for environment separation
7. **Implement proper monitoring** and logging
8. **Configure network policies** for security
9. **Use image scanning** and security policies
10. **Set up backup and disaster recovery**

## Architecture

The deployment creates:

- **3 replicas** of the Django application (configurable)
- **ClusterIP service** for internal access
- **ConfigMap** for non-sensitive configuration
- **Secret** for sensitive data (base64 encoded)
- **Health checks** for automatic pod management
- **Resource limits** for resource management
