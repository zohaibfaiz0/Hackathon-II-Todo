# Data Model: Kubernetes Deployment for Hackathon Todo App

## Kubernetes Entities

### Backend Deployment
- **Type**: Deployment
- **Replicas**: 1
- **Image**: todo-backend:latest
- **Ports**: 8000 (internal)
- **Environment Variables**:
  - DATABASE_URL: Connection string to PostgreSQL service
  - GEMINI_API_KEY: API key for Gemini integration
  - SECRET_KEY: Application secret key
  - ALLOWED_ORIGINS: Frontend service URL
- **Resource Requirements**: Minimal (for local development)

### Backend Service
- **Type**: ClusterIP
- **Port**: 8000
- **Target Port**: 8000
- **Purpose**: Internal access to backend API from frontend

### Frontend Deployment
- **Type**: Deployment
- **Replicas**: 1
- **Image**: todo-frontend:latest
- **Ports**: 3000 (internal)
- **Environment Variables**:
  - NEXT_PUBLIC_API_URL: URL to backend service
- **Resource Requirements**: Minimal (for local development)

### Frontend Service
- **Type**: NodePort
- **Port**: 3000
- **Target Port**: 3000
- **Node Port**: Dynamic assignment
- **Purpose**: External access to frontend from browser

### PostgreSQL StatefulSet
- **Type**: StatefulSet
- **Replicas**: 1
- **Image**: postgres:15
- **Ports**: 5432
- **Environment Variables**:
  - POSTGRES_USER: Database user
  - POSTGRES_PASSWORD: Database password (from Secret)
  - POSTGRES_DB: Database name
- **Persistent Volume**: 1GB claim for data persistence
- **Resource Requirements**: Minimal (for local development)

### PostgreSQL Service
- **Type**: ClusterIP
- **Port**: 5432
- **Target Port**: 5432
- **Purpose**: Internal access to database from backend

### Secrets
- **Type**: Kubernetes Secret
- **Key-Value Pairs**:
  - gemini_api_key: Encoded Gemini API key
  - db_password: Encoded database password
  - secret_key: Encoded application secret key

### ConfigMaps (Optional)
- **Type**: Kubernetes ConfigMap
- **Purpose**: Non-sensitive configuration values that can be changed without rebuilding images
- **Values**: Hostnames, ports, and other configuration parameters

## Relationships
- Frontend Deployment → Frontend Service (owns)
- Backend Deployment → Backend Service (owns)
- PostgreSQL StatefulSet → PostgreSQL Service (owns)
- Deployments → Secrets (references for environment variables)
- Backend Service ↔ PostgreSQL Service (network communication)
- Frontend Service ↔ Backend Service (network communication)