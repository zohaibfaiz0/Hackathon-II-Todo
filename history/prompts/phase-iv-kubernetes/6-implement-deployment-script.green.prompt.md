---
id: 6
title: Create deployment script
stage: green
date: 2026-02-08
surface: agent
model: Haiku 4.5
feature: phase-iv-kubernetes
branch: main
user: zohaibfaiz0
command: /sp.implement
labels: [kubernetes, minikube, helm, deployment, automation, script]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - deploy/local-setup.sh
tests:
 - none
---

## Prompt

/sp.implement

```
# Implement T015: Create Deployment Script & Verify

## Task
Create a script to automate local Minikube deployment.

## File: deploy/local-setup.sh
Create this file with executable permissions:

```bash
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
```

## Verify All Files
Run this check to confirm all Phase 2 files exist:
```bash
ls -la deploy/local-setup.sh
ls -la deploy/k8s/helm/todo-app/
ls -la deploy/k8s/helm/todo-app/templates/
```
```

## Response snapshot

Created deploy/local-setup.sh with executable permissions. The script automates:
- Starting Minikube with Docker driver
- Switching Docker context to Minikube
- Building backend and frontend Docker images
- Deploying Helm chart with test secrets
- Providing port-forward instructions for local access

All required files verified:
- local-setup.sh (executable)
- Helm chart with Chart.yaml, values.yaml
- All templates: backend/postgres/frontend deployments and services, secrets

## Outcome

- ✅ Impact: Local deployment automation ready for testing
- 🧪 Tests: none
- 📁 Files: 1 file created (deploy/local-setup.sh)
- 🔁 Next prompts: Test the deployment script; add production deployment script with proper secrets management
- 🧠 Reflection: Simple automation script encapsulates the entire local setup workflow, making it easy to spin up the full stack

## Evaluation notes (flywheel)

- Failure modes observed: None - straightforward script creation based on clear specification
- Graders run and results (PASS/FAIL): PASS - Script created with all required steps; all Phase 2 files verified present
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Test script execution in actual Minikube environment to identify any missing dependencies or configuration issues
