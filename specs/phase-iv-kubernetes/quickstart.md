# Quickstart Guide: Kubernetes Deployment

## Prerequisites

1. Install Docker Desktop (with Kubernetes support) or Minikube
2. Install Helm 3.x
3. Install kubectl
4. Clone the hackathon-todo repository

## Setup Instructions

### 1. Start Minikube
```bash
minikube start
```

### 2. Configure Docker Environment
Point your Docker CLI to Minikube's container registry:
```bash
eval $(minikube -p minikube docker-env)
```

### 3. Build Container Images
Build the backend and frontend container images:
```bash
# Build backend image
docker build -t todo-backend:latest ./backend

# Build frontend image
docker build -t todo-frontend:latest ./frontend
```

### 4. Create Kubernetes Secrets
Create the required secrets for database password, Gemini API key, and application secret:
```bash
kubectl create secret generic todo-secrets \
  --from-literal=gemini_api_key=<YOUR_GEMINI_API_KEY> \
  --from-literal=db_password=<YOUR_DB_PASSWORD> \
  --from-literal=secret_key=<YOUR_SECRET_KEY>
```

### 5. Deploy with Helm
Install the application using the Helm chart:
```bash
helm install todo-app ./deploy/k8s/helm/todo-app
```

### 6. Access the Application
Get the frontend URL:
```bash
minikube service todo-frontend --url
```

Or use port forwarding:
```bash
kubectl port-forward svc/todo-frontend 3000:3000
kubectl port-forward svc/todo-backend 8000:8000
```

Then access the application at http://localhost:3000

## Troubleshooting

### Check Pod Status
```bash
kubectl get pods
```

### View Logs
```bash
kubectl logs -l app=backend
kubectl logs -l app=frontend
kubectl logs -l app=postgres
```

### Verify Services
```bash
kubectl get services
```

### Clean Up
```bash
helm uninstall todo-app
kubectl delete secret todo-secrets
```