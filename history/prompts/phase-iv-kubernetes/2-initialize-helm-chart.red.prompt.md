---
id: 2
title: Initialize Helm chart structure for todo-app
stage: red
date: 2026-02-07
surface: agent
model: claude-sonnet-4-5
feature: phase-iv-kubernetes
branch: main
user:
command: sp.implement
labels: [helm, kubernetes, initialization]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - deploy/k8s/helm/todo-app/Chart.yaml
 - deploy/k8s/helm/todo-app/values.yaml
tests:
---

## Prompt

# Implement T-403: Initialize Helm Chart

## Task
Initialize the Helm Chart structure for the Todo App.

## Directory Structure
Create directories:
`deploy/k8s/helm/todo-app/`
`deploy/k8s/helm/todo-app/templates/`

## File 1: Chart.yaml
**Location:** `deploy/k8s/helm/todo-app/Chart.yaml`

```yaml
apiVersion: v2
name: todo-app
description: A Helm chart for Hackathon Todo App (FastAPI + Next.js + Postgres)
type: application
version: 0.1.0
appVersion: "1.0.0"
```

## File 2: values.yaml
**Location:** `deploy/k8s/helm/todo-app/values.yaml`

This file defines all the default configuration.

```yaml
# Global settings
nameOverride: ""
fullnameOverride: ""

# Backend Configuration
backend:
  replicaCount: 1
  image:
    repository: todo-backend
    pullPolicy: IfNotPresent
    tag: "latest"
  service:
    type: ClusterIP
    port: 8000
  env:
    # DATABASE_URL will be constructed from postgres settings
    ALLOWED_ORIGINS: "*"
  # Secrets will be injected via secrets.yaml template

# Frontend Configuration
frontend:
  replicaCount: 1
  image:
    repository: todo-frontend
    pullPolicy: IfNotPresent
    tag: "latest"
  service:
    type: NodePort
    port: 3000
    nodePort: 30000  # Fixed port for easy access via Minikube IP
  env:
    # NEXT_PUBLIC_API_URL needs to point to backend
    # In Minikube, this might need adjustment based on how you access it
    # For local dev via port-forward, localhost:8000 works
    NEXT_PUBLIC_API_URL: "http://localhost:8000"

# Postgres Configuration
postgres:
  image:
    repository: postgres
    pullPolicy: IfNotPresent
    tag: "15-alpine"
  storage:
    size: 1Gi
    className: standard
  auth:
    username: todo_user
    database: todo_db
    # Password should be provided via secret, defaulting here for dev only
    password: "secure_password_dev_only"
  service:
    port: 5432
```

## Verification
Run this to confirm files are created:
```bash
ls -la deploy/k8s/helm/todo-app/
cat deploy/k8s/helm/todo-app/Chart.yaml
cat deploy/k8s/helm/todo-app/values.yaml
```

## Response snapshot

Created complete Helm chart structure for Hackathon Todo App with:
- Chart.yaml: Proper Helm chart metadata and description
- values.yaml: Complete configuration for all three components:
  - Backend: FastAPI service with ClusterIP
  - Frontend: Next.js service with NodePort (30000)
  - Postgres: Database with 1Gi storage
- Created directory structure: deploy/k8s/helm/todo-app/ and templates/

## Outcome

- ✅ Impact: Successfully initialized Helm chart structure with all required configuration
- 🧪 Tests: Created both Chart.yaml and values.yaml with proper structure
- 🗁 Files: Created Helm chart directories and configuration files
- 🔄 Next prompts: Implement Kubernetes templates (StatefulSet, Services, Secrets)
- 🧠 Reflection: Helm chart structure properly separates configuration from implementation templates

## Evaluation notes (flywheel)

- Failure modes observed: N/A
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Implement PostgreSQL StatefulSet template