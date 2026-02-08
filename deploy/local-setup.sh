#!/bin/bash
set -e

echo "🚀 Starting Local Kubernetes Setup..."

# 1. Start Minikube (if not running)
if ! minikube status | grep -q "Running"; then
    minikube start --driver=docker
fi

# 2. Switch to Minikube's Docker daemon
echo "🔌 Switching to Minikube Docker context..."
eval $(minikube -p minikube docker-env)

# 3. Build Images (inside Minikube)
echo "📦 Building Backend Image..."
docker build -t todo-backend:latest ../backend

echo "📦 Building Frontend Image..."
docker build -t todo-frontend:latest ../frontend

# 4. Install/Upgrade Helm Chart
echo "☸️  Deploying to Kubernetes..."
# Ensure secrets are passed (using placeholder for now, replace in prod)
helm upgrade --install todo-app ./k8s/helm/todo-app \
  --set backend.secrets.geminiApiKey="${GEMINI_API_KEY:-fake-key}" \
  --set backend.secrets.secretKey="dev-secret-key"

echo "✅ Deployment initiated!"
echo ""
echo "👉 To access the app, run these commands in separate terminals:"
echo "   kubectl port-forward svc/todo-app-frontend 3000:3000"
echo "   kubectl port-forward svc/todo-app-backend 8000:8000"
echo ""
echo "🌍 Frontend: http://localhost:3000"
echo "🔌 Backend: http://localhost:8000/docs"
