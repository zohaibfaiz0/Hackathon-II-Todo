---
id: 1
title: K8s Deployment Spec
stage: spec
date: 2026-02-07
surface: agent
model: claude-opus-4-6
feature: phase-iv-kubernetes
branch: main
user: unknown
command: /sp.specify
labels: ["k8s", "deployment", "specification", "containerization", "helm"]
links:
  spec: specs/phase-iv-kubernetes/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/phase-iv-kubernetes/spec.md
 - specs/phase-iv-kubernetes/checklists/requirements.md
tests:
 - none
---

## Prompt

- Phase 4: Local Kubernetes Deployment

Create specification at: specs/phase-iv-kubernetes/spec.md

## Context
- Project: Hackathon Todo App
- Current State: Phase 3 complete (Python FastAPI + Next.js)
- Goal: Deploy to local Kubernetes (Minikube) using Helm

## 1. Containerization Requirements
We need to containerize the application components:

### Backend Container
- Base Image: `python:3.12-slim` (or 3.13)
- Build Tool: `uv` for dependency management
- Port: Expose 8000
- Command: `uv run uvicorn src.hackathon_todo_api.main:app --host 0.0.0.0 --port 8000`
- Optimization: Multi-stage build to keep image small

### Frontend Container
- Base Image: `node:20-alpine`
- Framework: Next.js 16+
- Build: `npm run build`
- Output: Standalone mode (for smaller image)
- Port: Expose 3000

## 2. Kubernetes Architecture (Minikube)

We need to deploy these components to a local cluster:

### A. Postgres Database
- **Type**: StatefulSet (because DBs need persistent storage)
- **Storage**: PersistentVolumeClaim (1GB is enough for local)
- **Service**: ClusterIP (internal access only)
- **Creds**: Use Kubernetes Secrets

### B. Backend Service
- **Type**: Deployment (1 replica)
- **Service**: ClusterIP
- **Env Vars**:
  - `DATABASE_URL`: Connection string to Postgres service
  - `GEMINI_API_KEY`: From K8s Secret
  - `SECRET_KEY`: From K8s Secret
  - `ALLOWED_ORIGINS`: Frontend URL

### C. Frontend Service
- **Type**: Deployment (1 replica)
- **Service**: NodePort (to access from your browser via localhost)
- **Env Vars**:
  - `NEXT_PUBLIC_API_URL`: URL to Backend Service

## 3. Configuration Management (Helm)
- Use a **Helm Chart** named `todo-app`.
- Structure:
  - `charts/`: Sub-charts (if needed)
  - `templates/`: K8s manifests (Deployments, Services, Secrets)
  - `values.yaml`: Central configuration file

## 4. AI DevOps Tooling
- We will use **kubectl-ai** to generate debugging commands.
- We will use **kagent** for cluster analysis.

## User Stories for Ops
- **US-401**: As a dev, I can build Docker images with `docker build`.
- **US-402**: As a dev, I can deploy the whole stack with `helm install`.
- **US-403**: As a dev, I can access the frontend via `localhost` (port forwarding).
- **US-404**: As a dev, database data persists if I restart the pods.

## Acceptance Criteria
- [ ] Dockerfiles created and build successfully
- [ ] Helm Chart created with templates for Backend, Frontend, and DB
- [ ] Application running on Minikube
- [ ] Frontend connects to Backend inside the cluster
- [ ] Chatbot works in the deployed version

## Response snapshot

Created a comprehensive specification for deploying the Hackathon Todo App to local Kubernetes using Minikube and Helm, including containerization requirements for both frontend and backend components, proper service configurations, and persistence setup for the database.

## Outcome

- ✅ Impact: Created complete feature specification for Kubernetes deployment with user stories, requirements, and success criteria
- 🧪 Tests: none
- 📁 Files: specs/phase-iv-kubernetes/spec.md, specs/phase-iv-kubernetes/checklists/requirements.md
- 🔁 Next prompts: /sp.plan to create implementation plan
- 🧠 Reflection: The specification comprehensively covers all deployment aspects from containerization to persistence requirements.

## Evaluation notes (flywheel)

- Failure modes observed: Script .specify/scripts/bash/create-phr.sh was not found, had to create PHR manually
- Graders run and results (PASS/FAIL): PASS - PHR created successfully with all required information
- Prompt variant (if applicable): Manual creation due to missing script
- Next experiment (smallest change to try): Verify if the script exists in a different location or needs to be created