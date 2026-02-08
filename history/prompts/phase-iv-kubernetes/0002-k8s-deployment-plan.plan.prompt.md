---
id: 2
title: K8s Deployment Plan
stage: plan
date: 2026-02-07
surface: agent
model: claude-opus-4-6
feature: phase-iv-kubernetes
branch: main
user: unknown
command: /sp.plan
labels: ["k8s", "deployment", "plan", "containerization", "helm", "architecture"]
links:
  spec: specs/phase-iv-kubernetes/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/phase-iv-kubernetes/plan.md
 - specs/phase-iv-kubernetes/research.md
 - specs/phase-iv-kubernetes/data-model.md
 - specs/phase-iv-kubernetes/quickstart.md
 - specs/phase-iv-kubernetes/contracts/api-contracts.md
tests:
 - none
---

## Prompt

- Phase 4: Kubernetes Technical Plan

Create plan at: specs/phase-iv-kubernetes/plan.md

## Reference
- Spec: @specs/phase-iv-kubernetes/spec.md

## 1. Directory Structure
We will add a `deploy/` folder to keep infrastructure separate from code:

```
hackathon-todo/
├── backend/
│   └── Dockerfile          # NEW
├── frontend/
│   └── Dockerfile          # NEW
├── deploy/                 # NEW
│   └── k8s/
│       └── helm/
│           └── todo-app/   # Main Chart
│               ├── Chart.yaml
│               ├── values.yaml
│               └── templates/
│                   ├── backend-deployment.yaml
│                   ├── backend-service.yaml
│                   ├── frontend-deployment.yaml
│                   ├── frontend-service.yaml
│                   ├── postgres-statefulset.yaml
│                   ├── postgres-service.yaml
│                   └── secrets.yaml
```

## 2. Docker Strategy

### Backend Dockerfile (Multi-stage)
1.  **Builder Stage**:
    *   Image: `python:3.12-slim`
    *   Install `uv`
    *   Copy `pyproject.toml` & `uv.lock`
    *   Run `uv sync` to install deps
2.  **Runner Stage**:
    *   Copy venv from Builder
    *   Copy source code (`src/`)
    *   CMD: `uv run uvicorn ...`

### Frontend Dockerfile (Multi-stage)
1.  **Builder Stage**:
    *   Image: `node:20-alpine`
    *   Install deps
    *   Run `npm run build`
2.  **Runner Stage**:
    *   Copy `.next/standalone` (optimized build)
    *   Copy `public/` and `static/`
    *   CMD: `node server.js`

## 3. Helm Chart Strategy

We will use a single Chart `todo-app` that manages all 3 components.

### `values.yaml` Configuration
Define defaults that can be overridden:
```yaml
postgres:
  storage: 1Gi
  user: todo_user
  db: todo_db

backend:
  image: todo-backend:latest
  replicas: 1
  port: 8000

frontend:
  image: todo-frontend:latest
  replicas: 1
  port: 3000
  serviceType: NodePort
```

### Networking Logic
*   **Internal**: Backend talks to Postgres via `postgres-service:5432`.
*   **External**: Browser talks to Frontend via `localhost:3000` (forwarded).
*   **Browser-to-Backend**: Browser needs to reach Backend API. We will map Backend to `localhost:8000` so the frontend client code (running in browser) can find it.

## 4. Deployment Workflow (Minikube)

1.  Start Minikube: `minikube start`
2.  Point shell to Minikube's Docker: `eval $(minikube -p minikube docker-env)`
3.  Build Images:
    *   `docker build -t todo-backend:latest ./backend`
    *   `docker build -t todo-frontend:latest ./frontend`
4.  Install Chart: `helm install todo-app ./deploy/k8s/helm/todo-app`
5.  Port Forwarding (to access from host):
    *   `kubectl port-forward svc/todo-frontend 3000:3000`
    *   `kubectl port-forward svc/todo-backend 8000:8000`

## 5. Security
*   **Secrets**: We will create a `secrets.yaml` template that pulls values from Base64 encoded strings (we will generate these during setup).
*   **Gitignore**: Ensure `secrets.yaml` or any file with real keys is ignored (though for this hackathon using a template with placeholders is acceptable).

## 6. Verification Plan
1.  **Pod Status**: `kubectl get pods` (All Running)
2.  **Logs**: `kubectl logs -l app=backend` (No crash loops)
3.  **Connectivity**: Access `http://localhost:3000`, login, verify data loads.

## Response snapshot

Created a comprehensive implementation plan for deploying the Hackathon Todo App to local Kubernetes using Minikube and Helm, including technical context, project structure, research, data models, and quickstart guide.

## Outcome

- ✅ Impact: Created complete technical plan with architecture decisions, research findings, data models, and deployment instructions
- 🧪 Tests: none
- 📁 Files: specs/phase-iv-kubernetes/plan.md, specs/phase-iv-kubernetes/research.md, specs/phase-iv-kubernetes/data-model.md, specs/phase-iv-kubernetes/quickstart.md, specs/phase-iv-kubernetes/contracts/api-contracts.md
- 🔁 Next prompts: /sp.tasks to create implementation tasks
- 🧠 Reflection: The plan provides a complete roadmap for containerizing the application and deploying it to Kubernetes with proper architecture decisions documented.

## Evaluation notes (flywheel)

- Failure modes observed: Script .specify/scripts/bash/create-phr.sh was not found, had to create PHR manually; PowerShell scripts could not execute due to missing pwsh
- Graders run and results (PASS/FAIL): PASS - PHR created successfully with all required information
- Prompt variant (if applicable): Manual creation due to missing script
- Next experiment (smallest change to try): Verify if the script exists in a different location or needs to be created