---
id: 5
title: Implement frontend templates
stage: green
date: 2026-02-08
surface: agent
model: Haiku 4.5
feature: phase-iv-kubernetes
branch: main
user: zohaibfaiz0
command: /sp.implement
labels: [kubernetes, helm, frontend, templates, deployment, service]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - deploy/k8s/helm/todo-app/templates/frontend-deployment.yaml
 - deploy/k8s/helm/todo-app/templates/frontend-service.yaml
tests:
 - none
---

## Prompt

/sp.implement

```
# Implement T012, T013: Frontend Templates

## Tasks
- **T013**: Create `frontend-service.yaml`
- **T012**: Create `frontend-deployment.yaml`

## 1. Implement T013: Frontend Service
**File:** `deploy/k8s/helm/todo-app/templates/frontend-service.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ include "todo-app.fullname" . }}-frontend
  labels:
    app: frontend
spec:
  type: {{ .Values.frontend.service.type }}
  ports:
    - port: {{ .Values.frontend.service.port }}
      targetPort: 3000
      protocol: TCP
      name: http
      {{- if eq .Values.frontend.service.type "NodePort" }}
      nodePort: {{ .Values.frontend.service.nodePort }}
      {{- end }}
  selector:
    app: frontend
```

## 2. Implement T012: Frontend Deployment
**File:** `deploy/k8s/helm/todo-app/templates/frontend-deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "todo-app.fullname" . }}-frontend
  labels:
    app: frontend
spec:
  replicas: {{ .Values.frontend.replicaCount }}
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
        - name: frontend
          image: "{{ .Values.frontend.image.repository }}:{{ .Values.frontend.image.tag }}"
          imagePullPolicy: {{ .Values.frontend.image.pullPolicy }}
          ports:
            - name: http
              containerPort: 3000
              protocol: TCP
          env:
            # Points to the backend service.
            # IMPORTANT: For client-side fetching in browser, this needs to be accessible from the browser.
            # In Minikube with port-forwarding, localhost:8000 is often used.
            # Or use relative path if ingress is set up (advanced).
            - name: NEXT_PUBLIC_API_URL
              value: {{ .Values.frontend.env.NEXT_PUBLIC_API_URL | quote }}
```

## Verification
```bash
ls -la deploy/k8s/helm/todo-app/templates/frontend*
```
```

## Response snapshot

Created both frontend template files:
- frontend-deployment.yaml: Helm template for Deployment with replicas, image configuration, container port 3000, and NEXT_PUBLIC_API_URL environment variable
- frontend-service.yaml: Helm template for Service exposing port and supporting NodePort type

Both templates follow the existing Helm chart structure and use Helm templating for configurable values.

## Outcome

- ✅ Impact: Added Helm templates for frontend deployment and service to the Kubernetes configuration
- 🧪 Tests: none
- 📁 Files: 2 files created (deploy/k8s/helm/todo-app/templates/frontend-deployment.yaml, deploy/k8s/helm/todo-app/templates/frontend-service.yaml)
- 🔁 Next prompts: Configure frontend values in Helm values.yaml; Test deployment with T012 and T013 tasks
- 🧠 Reflection: Standard Helm deployment pattern successfully applied to frontend service, matching backend structure

## Evaluation notes (flywheel)

- Failure modes observed: PHR creation script not available on Windows (PowerShell only); created file manually
- Graders run and results (PASS/FAIL): PASS - Both template files created to spec
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Add values.yaml configuration for frontend and run Helm template linting
