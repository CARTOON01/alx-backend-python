# Kubernetes Setup Script (kurbeScript)

This script automates the setup and verification of a local Kubernetes cluster using Minikube.

## Prerequisites

- Linux system (Ubuntu/Debian recommended)
- Docker installed and running
- Internet connection for downloading dependencies

## What the Script Does

1. **Checks Dependencies**: Verifies that Docker is installed and installs Minikube and kubectl if they're not present
2. **Starts Cluster**: Launches a local Kubernetes cluster using Minikube with Docker driver
3. **Verifies Cluster**: Runs `kubectl cluster-info` to ensure the cluster is working properly
4. **Retrieves Pods**: Lists all available pods in all namespaces and the default namespace
5. **Shows Status**: Displays comprehensive cluster status information

## Usage

```bash
# Make the script executable (if not already done)
chmod +x kurbeScript

# Run the script
./kurbeScript
```

## Features

- **Automatic Installation**: Installs Minikube and kubectl if not present
- **Cross-platform Support**: Detects OS and architecture automatically
- **Comprehensive Verification**: Checks cluster health and connectivity
- **Detailed Output**: Color-coded status messages and comprehensive information
- **Error Handling**: Exits gracefully on errors with helpful messages

## Sample Output

The script provides colored output showing:
- Installation progress
- Cluster startup status
- Cluster information from `kubectl cluster-info`
- All available pods
- Node and service information
- Helpful commands for future use

## Troubleshooting

If you encounter issues:

1. **Docker not running**: Start Docker service
   ```bash
   sudo systemctl start docker
   ```

2. **Permission issues**: Add your user to the docker group
   ```bash
   sudo usermod -aG docker $USER
   ```

3. **Minikube won't start**: Try deleting and recreating the cluster
   ```bash
   minikube delete
   ./kurbeScript
   ```

## Useful Commands After Setup

- `kubectl get nodes` - List cluster nodes
- `kubectl get pods --all-namespaces` - List all pods
- `minikube dashboard` - Open web dashboard
- `minikube stop` - Stop the cluster
- `minikube delete` - Delete the cluster

## Requirements Met

✅ Starts a Kubernetes cluster on your machine  
✅ Verifies cluster is running using `kubectl cluster-info`  
✅ Retrieves available pods  
✅ Ensures Minikube is installed  
