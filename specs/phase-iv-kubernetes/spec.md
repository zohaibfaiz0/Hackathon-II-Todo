# Feature Specification: Kubernetes Deployment

**Feature Branch**: `phase-iv-kubernetes`
**Created**: 2026-02-07
**Status**: Draft
**Input**: User description: "
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
- [ ] Chatbot works in the deployed version"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Deploy Application Stack (Priority: P1)

As a developer, I want to deploy the entire Hackathon Todo App stack to a local Kubernetes cluster using Helm, so that I can test the application in a production-like environment.

**Why this priority**: This is the core functionality that enables local Kubernetes deployment, which is the primary goal of this feature.

**Independent Test**: Can be fully tested by running `helm install` command and verifying that all services are running and accessible, delivering a complete working application.

**Acceptance Scenarios**:

1. **Given** a running Minikube cluster, **When** I run `helm install todo-app ./charts/todo-app`, **Then** all services (frontend, backend, database) are deployed and running
2. **Given** the deployed application, **When** I access the frontend via NodePort, **Then** I can interact with the full application functionality including the chatbot

---

### User Story 2 - Build Container Images (Priority: P2)

As a developer, I want to build optimized container images for the frontend and backend components, so that I can deploy lightweight and secure containers to Kubernetes.

**Why this priority**: Containerization is a prerequisite for Kubernetes deployment and ensures proper packaging of the application.

**Independent Test**: Can be fully tested by running `docker build` commands for both frontend and backend and verifying successful image creation with appropriate base images and configurations.

**Acceptance Scenarios**:

1. **Given** the application source code, **When** I run `docker build` for the backend, **Then** an image based on `python:3.12-slim` with `uv` installed is created and exposes port 8000
2. **Given** the application source code, **When** I run `docker build` for the frontend, **Then** an image based on `node:20-alpine` with Next.js built and ready to serve is created and exposes port 3000

---

### User Story 3 - Persist Database Data (Priority: P3)

As a developer, I want the database to persist data across pod restarts, so that application data is not lost when Kubernetes deployments are updated or pods are restarted.

**Why this priority**: Data persistence is critical for maintaining application state and ensuring a reliable user experience during deployments.

**Independent Test**: Can be verified by inserting data into the database, restarting the database pod, and confirming the data remains intact.

**Acceptance Scenarios**:

1. **Given** a running database in Kubernetes, **When** I insert data and restart the database pod, **Then** the data persists and remains accessible
2. **Given** a configured StatefulSet with PersistentVolumeClaim, **When** the database pod is recreated, **Then** it mounts the same persistent storage volume

---

### Edge Cases

- What happens when Minikube resources are insufficient for the application?
- How does the system handle database connection failures during startup?
- What occurs when Helm chart values are misconfigured?
- How does the system behave when the cluster is under high load?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST containerize the backend service using Python 3.12-slim base image with uv dependency manager
- **FR-002**: System MUST containerize the frontend service using node:20-alpine base image with Next.js 16+ built in standalone mode
- **FR-003**: System MUST deploy the database as a StatefulSet with PersistentVolumeClaim for data persistence
- **FR-004**: System MUST expose the backend service internally using ClusterIP service
- **FR-005**: System MUST expose the frontend service externally using NodePort service
- **FR-006**: System MUST manage sensitive configuration using Kubernetes Secrets
- **FR-007**: System MUST provide a Helm chart named `todo-app` with configurable values
- **FR-008**: System MUST support deployment via `helm install` command
- **FR-009**: System MUST configure proper environment variables for inter-service communication
- **FR-010**: System MUST ensure the frontend can connect to the backend service within the cluster
- **FR-011**: System MUST ensure the backend can connect to the database service within the cluster

### Key Entities

- **Backend Container**: Python FastAPI application container that serves the API, configured with proper dependencies and startup command
- **Frontend Container**: Next.js application container that serves the UI, built in standalone mode for minimal size
- **Database StatefulSet**: PostgreSQL database deployment with persistent storage that maintains identity and stable network identifiers
- **Helm Chart**: Package of Kubernetes manifests that defines the entire application stack with configurable parameters
- **Kubernetes Secrets**: Secure storage for sensitive configuration like API keys and database credentials

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Developers can successfully deploy the entire application stack to Minikube using a single Helm command in under 5 minutes
- **SC-002**: All services (frontend, backend, database) are operational and communicating within the Kubernetes cluster after deployment
- **SC-003**: Database data persists across pod restarts and deployment updates with 100% retention
- **SC-004**: Frontend successfully connects to backend API within the cluster and displays the chatbot functionality
- **SC-005**: Container images build successfully with optimized sizes (backend under 200MB, frontend under 150MB)
- **SC-006**: Application remains accessible via localhost through NodePort service after deployment