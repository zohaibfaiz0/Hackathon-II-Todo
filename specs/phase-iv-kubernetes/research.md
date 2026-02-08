# Research: Kubernetes Deployment for Hackathon Todo App

## Decision: Container Base Images
**Rationale**: Using official, minimal base images reduces attack surface and image size. Python 3.12-slim and Node 20-alpine are industry standard choices that align with the existing technology stack.

**Alternatives considered**:
- Larger Python base images (unnecessary bloat)
- Different Node versions (20-alpine is current and lightweight)

## Decision: Multi-stage Docker Builds
**Rationale**: Multi-stage builds significantly reduce final image size by separating build dependencies from runtime dependencies. This follows Docker best practices and optimizes for both security and performance.

**Alternatives considered**:
- Single-stage builds (larger images with unnecessary build tools in runtime)
- Pre-built application packages (less control and flexibility)

## Decision: StatefulSet for PostgreSQL
**Rationale**: StatefulSets provide stable network identities and persistent storage, which are essential for database workloads. Unlike Deployments, StatefulSets guarantee ordered pod creation/deletion and maintain persistent storage associations.

**Alternatives considered**:
- Deployment with PersistentVolume (no stable network identity)
- External database (defeats purpose of self-contained deployment)

## Decision: Service Types (ClusterIP vs NodePort)
**Rationale**: Backend service uses ClusterIP for internal communication only, while frontend uses NodePort to allow external access. This follows security best practices by limiting exposure of internal services.

**Alternatives considered**:
- Both using NodePort (exposes backend unnecessarily)
- Both using ClusterIP (no external access to frontend)

## Decision: Helm for Configuration Management
**Rationale**: Helm provides templating, versioning, and release management for Kubernetes applications. It allows parameterized deployments and simplifies complex application management.

**Alternatives considered**:
- Raw Kubernetes manifests (no parameterization or versioning)
- Kustomize (less mature templating than Helm)

## Decision: Environment Variables for Configuration
**Rationale**: Using environment variables passed from Kubernetes ConfigMaps/Secrets to pods is the standard Kubernetes pattern for configuration. This keeps configuration external to the application and allows different values per environment.

**Alternatives considered**:
- Configuration files mounted as volumes (more complex management)
- Hardcoded values (no flexibility)

## Deployment Workflow Research
**Finding**: The workflow requires building images in the Minikube Docker environment to ensure they're available to the local cluster. This is a standard Minikube pattern that avoids pushing to external registries for local development.

**Best Practice**: Using `eval $(minikube -p minikube docker-env)` temporarily points Docker CLI to Minikube's container daemon, allowing direct image building into the cluster.