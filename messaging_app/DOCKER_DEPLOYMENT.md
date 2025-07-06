# Docker Deployment Guide

This guide explains how to set up GitHub Actions for building and pushing Docker images to Docker Hub.

## Prerequisites

1. **Docker Hub Account**: You need a Docker Hub account to push images.
2. **GitHub Repository**: Your code should be in a GitHub repository.

## Setup Instructions

### 1. Configure GitHub Secrets

You need to add the following secrets to your GitHub repository:

1. Go to your GitHub repository
2. Click on **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** and add these secrets:

| Secret Name | Description | Example Value |
|-------------|-------------|---------------|
| `DOCKER_USERNAME` | Your Docker Hub username | `johndoe` |
| `DOCKER_PASSWORD` | Your Docker Hub password or access token | `your-password-here` |

**Security Tip**: Instead of using your Docker Hub password, create an access token:
1. Go to Docker Hub → Account Settings → Security
2. Click "New Access Token"
3. Use this token as your `DOCKER_PASSWORD`

### 2. Workflow Triggers

The GitHub Actions workflow (`dep.yml`) will automatically trigger on:
- Push to `main`, `develop`, or `master` branches
- Pull requests to `main`, `develop`, or `master` branches
- GitHub releases

### 3. Docker Image Tags

The workflow automatically creates multiple tags for your Docker image:
- `latest` (for main branch)
- `<branch-name>` (for other branches)
- `<branch-name>-<commit-sha>` (for all commits)
- `v<version>` (for releases)

### 4. What the Workflow Does

1. **Builds** the Docker image using the provided Dockerfile
2. **Tests** the image by running a container
3. **Pushes** to Docker Hub (only for non-PR events)
4. **Scans** for security vulnerabilities using Trivy
5. **Supports** multi-platform builds (AMD64 and ARM64)

## Local Docker Commands

### Build the image locally:
```bash
docker build -t messaging-app .
```

### Run the container:
```bash
docker run -p 8000:8000 messaging-app
```

### Push to Docker Hub (after building):
```bash
docker tag messaging-app your-username/messaging-app:latest
docker push your-username/messaging-app:latest
```

## Dockerfile Explanation

The provided Dockerfile:
- Uses Python 3.11 slim base image
- Installs system dependencies for MySQL
- Installs Python dependencies from requirements.txt
- Creates a non-root user for security
- Exposes port 8000
- Uses Gunicorn as the WSGI server

## Environment Variables

When running the container in production, you may need to set:
- `DJANGO_SETTINGS_MODULE=messaging_app.settings`
- `SECRET_KEY=your-secret-key`
- `DATABASE_URL=your-database-url`
- `DEBUG=False`

## Troubleshooting

### Common Issues:

1. **Authentication Error**: Check that your Docker Hub credentials are correct in GitHub secrets
2. **Build Fails**: Ensure all dependencies in requirements.txt are available
3. **Permission Denied**: Make sure your Docker Hub account has push permissions

### Viewing Logs:
- Go to your GitHub repository → Actions tab
- Click on the workflow run to see detailed logs

## Security Features

The workflow includes:
- Multi-platform builds for better compatibility
- Security vulnerability scanning with Trivy
- Non-root user in Docker container
- Secure secret management through GitHub Secrets
