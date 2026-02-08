---
id: 4
title: Create PostgreSQL StatefulSet and Service templates
stage: red
date: 2026-02-07
surface: agent
model: claude-sonnet-4-5
feature: phase-iv-kubernetes
branch: main
user:
command: sp.implement
labels: [helm, kubernetes, postgres]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - deploy/k8s/helm/todo-app/templates/postgres-service.yaml
 - deploy/k8s/helm/todo-app/templates/postgres-statefulset.yaml
tests:
---

## Prompt

# Implement T008 & T009: Postgres Templates

## Tasks
- **T008**: Create `postgres-statefulset.yaml`
- **T009**: Create `postgres-service.yaml`

## 1. Implement T009: Postgres Service (Headless)
**File:** `deploy/k8s/helm/todo-app/templates/postgres-service.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ include "todo-app.fullname" . }}-postgres
  labels:
    app: postgres
spec:
  ports:
    - port: {{ .Values.postgres.service.port }}
  selector:
    app: postgres
  clusterIP: None  # Headless service for StatefulSet
```

## 2. Implement T008: Postgres StatefulSet
**File:** `deploy/k8s/helm/todo-app/templates/postgres-statefulset.yaml`

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: {{ include "todo-app.fullname" . }}-postgres
spec:
  serviceName: {{ include "todo-app.fullname" . }}-postgres
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
        - name: postgres
          image: "{{ .Values.postgres.image.repository }}:{{ .Values.postgres.image.tag }}"
          ports:
            - containerPort: 5432
              name: postgres
          env:
            - name: POSTGRES_USER
              value: {{ .Values.postgres.auth.username }}
            - name: POSTGRES_PASSWORD
              value: {{ .Values.postgres.auth.password }}
            - name: POSTGRES_DB
              value: {{ .Values.postgres.auth.database }}
          volumeMounts:
            - name: data
              mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes: [ "ReadWriteOnce" ]
        storageClassName: {{ .Values.postgres.storage.className }}
        resources:
          requests:
            storage: {{ .Values.postgres.storage.size }}
```

## Verification
```bash
ls -la deploy/k8s/helm/todo-app/templates/postgres*
```

## Response snapshot

Created complete PostgreSQL deployment templates for Helm chart:
- **postgres-service.yaml**: Headless Service for StatefulSet communication
- **postgres-statefulset.yaml**: StatefulSet with 1 replica and PersistentVolumeClaim

Both templates properly use Helm template functions and values from values.yaml:
- Service: ClusterIP: None, proper selector and port
- StatefulSet: Proper metadata, container configuration, environment variables
- VolumeClaimTemplate: 1Gi storage with ReadWriteOnce access mode
- Proper label matching between Service and StatefulSet

## Outcome

- ✅ Impact: Successfully created PostgreSQL deployment templates with proper Kubernetes patterns
- 🧪 Tests: Created both StatefulSet and Service templates with correct configuration
- 🗁 Files: Added postgres-service.yaml and postgres-statefulset.yaml to templates/
- 🔄 Next prompts: Implement backend/frontend deployment templates
- 🧠 Reflection: StatefulSet with headless service is proper pattern for database deployment

## Evaluation notes (flywheel)

- Failure modes observed: N/A
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Add readiness/liveness probes to StatefulSet