---
id: 3
title: Initialize Helm chart foundation files
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
 - deploy/k8s/helm/todo-app/templates/_helpers.tpl
tests:
---

## Prompt

# Implement T005, T006, T007: Helm Foundation

## Tasks
- **T005**: Create `Chart.yaml`
- **T006**: Create `values.yaml`
- **T007**: Create `templates/` directory

## Directory
deploy/k8s/helm/todo-app/

## 1. Implement T005: Chart.yaml
**File:** `deploy/k8s/helm/todo-app/Chart.yaml`

```yaml
apiVersion: v2
name: todo-app
description: A Helm chart for Hackathon Todo App (FastAPI + Next.js + Postgres)
type: application
version: 0.1.0
appVersion: "1.0.0"
```

## 2. Implement T006: values.yaml
**File:** `deploy/k8s/helm/todo-app/values.yaml`

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
    ALLOWED_ORIGINS: "*"

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
    nodePort: 30000
  env:
    # Points to backend service internally or via localhost for browser
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
    # Password will be overridden by secret, this is default
    password: "secure_password_dev_only"
  service:
    port: 5432
```

## 3. Implement T007: Templates Directory
Create the directory `deploy/k8s/helm/todo-app/templates/`

## 4. Helper Template (Required for valid chart)
**File:** `deploy/k8s/helm/todo-app/templates/_helpers.tpl`

```yaml
{{/*
Expand the name of the chart.
*/}}
{{- define "todo-app.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "todo-app.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}
```

## Verification
```bash
ls -la deploy/k8s/helm/todo-app/
cat deploy/k8s/helm/todo-app/Chart.yaml
```

## Response snapshot

Created complete Helm chart foundation with:
- Chart.yaml: Proper Helm v2 chart metadata with description
- values.yaml: Complete configuration for all three services:
  - Backend: FastAPI service with ClusterIP and ALLOWED_ORIGINS
  - Frontend: Next.js service with NodePort (30000) and API URL
  - Postgres: Database with 1Gi storage and default credentials
- templates/ directory: Empty directory for Kubernetes manifests
- _helpers.tpl: Required helper templates for chart name and fullname

## Outcome

- ✅ Impact: Successfully created complete Helm chart foundation with all required files
- 🧪 Tests: Created Chart.yaml, values.yaml, templates/ directory, and _helpers.tpl
- 🗁 Files: All Helm chart foundation files properly structured and valid
- 🔄 Next prompts: Implement Kubernetes deployment manifests (T008-T014)
- 🧠 Reflection: Helm chart foundation properly separates configuration from implementation templates

## Evaluation notes (flywheel)

- Failure modes observed: N/A
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Implement PostgreSQL StatefulSet template