# Feature Specification: Event-Driven Architecture with Dapr & Redpanda

**Feature Branch**: `phase-v-cloud`
**Created**: 2026-02-08
**Status**: Draft
**Parent**: Phase IV - Kubernetes Deployment

## Context
- **Project**: Hackathon Todo App (FastAPI + Next.js + PostgreSQL)
- **Current State**: Phase 4 complete - application deployed to Kubernetes via Helm
- **Goal**: Introduce event-driven architecture using Dapr sidecars and Redpanda (Kafka-compatible) for pub/sub messaging

## 1. Feature Overview

### 1.1 Description
Extend the Kubernetes-deployed Hackathon Todo App with an event-driven architecture. This involves deploying Redpanda as the event bus via Helm, configuring Dapr sidecars for Pub/Sub and Service Invocation capabilities, and implementing event publishing and subscription for task creation events.

### 1.2 Goals
- Deploy Redpanda (Kafka-compatible) as the distributed event streaming platform
- Enable Dapr sidecars for both frontend and backend deployments
- Implement event publishing when tasks are created
- Implement event subscription to log task creation events
- Enable Service Invocation via Dapr for frontend-to-backend communication

### 1.3 Success Criteria
- Redpanda is deployed and operational in the Kubernetes cluster
- Dapr sidecars are injected and running alongside both frontend and backend pods
- Task creation events are published to Redpanda
- Task creation events are consumed and logged by the backend
- Frontend can invoke backend APIs via Dapr Service Invocation

## 2. User Stories

### US-501: Publish Task Creation Events to Event Bus

**As a** backend service,
**I want** to publish a `task.created` event when a task is created,
**So that** other services can react to task creation events.

**Acceptance Criteria:**
- Backend publishes `task.created` event to Redpanda topic `tasks` upon task creation
- Event payload includes: task_id, user_id, title, description, created_at
- Publishing uses Dapr HTTP API for Pub/Sub
- Publishing is non-blocking to task creation flow (fire-and-forget)
- Publishing failures are logged but do not prevent task creation

### US-502: Consume Task Creation Events

**As a** backend service,
**I want** to subscribe to `task.created` events from the event bus,
**So that** I can log and process task creation events.

**Acceptance Criteria:**
- Backend exposes endpoint `/api/events/task-created` for Dapr event delivery
- Dapr subscribes to `tasks` topic and routes events to the endpoint
- Event payload is validated upon receipt
- Events are logged with timestamp and metadata
- Endpoint returns 200 OK to acknowledge event processing

### US-503: Invoke Backend via Dapr Service Invocation

**As a** frontend application,
**I want** to call the backend API via Dapr sidecar,
**So that** I can leverage Dapr's service discovery and resilience features.

**Acceptance Criteria:**
- Frontend calls backend API endpoints using Dapr HTTP API format
- Dapr sidecar URL is `http://localhost:3500/v1.0/invoke/backend/method/...`
- Service discovery resolves to backend service within the cluster
- Requests failover and retry through Dapr's built-in resilience
- Frontend backend calls work identically to direct HTTP calls

## 3. Technical Requirements

### 3.1 Architecture
- **Event Bus**: Redpanda (Kafka-compatible) deployed via Helm
- **Dapr Runtime**: Dapr sidecar injection via Dapr Injector
- **Dapr Components**: Pub/Sub and Service Invocation
- **Deployment**: Kubernetes with existing Helm chart extended

### 3.2 Redpanda Requirements
- **Deployment Method**: Helm chart dependency in existing Chart.yaml
- **Version**: Latest stable Redpanda chart compatible with Kubernetes 1.28+
- **Persistence**: Enabled for event bus durability
- **Resource Limits**: Configurable via values (defaults for local development)
- **Brokers**: Single broker (minimal) for local development

### 3.3 Dapr Requirements
- **Injection**: enabled via `dapr.io/enabled: "true"` annotation
- **App IDs**: `backend` and `frontend` configured in annotations
- **API Version**: Dapr HTTP API v1.0
- **Components**: Configured via Kubernetes manifests
- **Placement**: Sidecar injected as container in each pod

### 3.4 Backend Requirements
- **Event Publishing**: On task creation route (`POST /api/tasks`)
- **Event Subscription**: New endpoint `/api/events/task-created`
- **HTTP Client**: Use `httpx` or similar async HTTP client for Dapr calls
- **Error Handling**: Log failures, non-blocking for main flow

### 3.5 Frontend Requirements
- **Service Invocation**: Update API calls to use Dapr invoke pattern
- **Base URL**: `http://localhost:3500/v1.0/invoke/backend/method/`
- **Path Mapping**: Map existing API paths to Dapr invoke format
- **Error Handling**: Leverage Dapr built-in retries and timeouts

### 3.6 Dapr Component Requirements

#### Pub/Sub Component (`pubsub.yaml`)
- **Type**: pubsub.redpanda
- **Topic**: `tasks`
- **Consumer Group**: `todo-backend`
- **SASL**: Disabled (local development)
- **TLS**: Optional (local development)

#### Subscription Component (`subscription.yaml`)
- **Topic**: `tasks`
- **Route**: `/api/events/task-created`
- **Pubsub Name**: `todo-pubsub`
- **Dead Letter Topic**: Optional

## 4. Event Schema

### task.created Event
```json
{
  "id": "evt_1234567890",
  "source": "todo-backend",
  "type": "task.created",
  "specversion": "1.0",
  "time": "2026-02-08T12:00:00Z",
  "datacontenttype": "application/json",
  "data": {
    "task_id": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": "660e8400-e29b-41d4-a716-446655440001",
    "title": "Sample task title",
    "description": "Sample task description",
    "completed": false,
    "created_at": "2026-02-08T12:00:00Z"
  }
}
```

## 5. API Specification

### 5.1 Dapr Pub/Sub API (Used by Backend)

**Publish Event**
- **URL**: `http://localhost:3500/v1.0/publish/pubsub-name/topic-name`
- **Method**: POST
- **Headers**: `Content-Type: application/cloudevents+json`
- **Body**: CloudEvents formatted event
- **Success Response**: 204 No Content

### 5.2 Event Subscription Endpoint

**Event Delivery**
- **URL**: `http://localhost:<port>/api/events/task-created`
- **Method**: POST
- **Headers**: `Content-Type: application/cloudevents+json`
- **Body**: CloudEvents formatted event (delivered by Dapr)
- **Success Response**: 200 OK

### 5.3 Dapr Service Invocation API (Used by Frontend)

**Invoke Backend Method**
- **URL**: `http://localhost:3500/v1.0/invoke/backend/method/<path>`
- **Method**: GET/POST/PATCH/DELETE (mirrors client request)
- **Headers**: `Content-Type: application/json` (as applicable)
- **Query Parameters**: Passed through to backend
- **Body**: Passed through to backend

**Path Mappings:**
- `/api/tasks` → `http://localhost:3500/v1.0/invoke/backend/method/api/tasks`
- `/api/tasks/{id}` → `http://localhost:3500/v1.0/invoke/backend/method/api/tasks/{id}`
- `/api/auth/login` → `http://localhost:3500/v1.0/invoke/backend/method/api/auth/login`

## 6. Dependencies

### External Dependencies
- **Redpanda Helm Chart**: charts.redpanda.com/redpanda
- **Dapr**: dapr.io/dapr Helm chart for cluster installation
  - Note: Dapr must be installed on the cluster first viaational deployment
- **Kubernetes**: 1.28+ (already present from Phase 4)

### Python Dependencies
- **httpx**: Async HTTP client for Dapr API calls
- Existing dependencies from Phase 4

### JavaScript/TypeScript Dependencies
- No additional dependencies beyond Phase 4
- Native fetch API sufficient for Dapr calls

### Helm Dependencies
- Existing chart structure from Phase 4
- Redpanda chart as dependency
- Dapr component templates

## 7. Implementation Constraints

### 7.1 Performance
- Event publishing should complete in under 100ms (non-blocking)
- Dapr sidecar adds minimal latency to service invocation (<10ms local)
- No impact on existing API performance for task operations

### 7.2 Scalability
- Redpanda configured for local development (single broker)
- Architecture supports horizontal scaling for production
- Event consumers can scale independently

### 7.3 Maintainability
- Dapr components managed as Kubernetes manifests
- Clear separation between event publishing and business logic
- Configurable via Helm values

### 7.4 Backwards Compatibility
- Frontend must retain ability for direct HTTP calls (fallback)
- Non-blocking event publishing ensures existing workflows unchanged
- Can be disabled via Helm values if needed

## 8. Security Considerations

### 8.1 Dapr Security
- Dapr sidecar runs in same Kubernetes pod (same security context)
- mTLS enabled by default for inter-service communication
- SASL auth optional for Redpanda (disabled for local dev)

### 8.2 Event Security
- Events contain user-scoped data (task_id, user_id)
- No sensitive data (passwords, tokens) in event payloads
- Event access controlled by Kubernetes RBAC

### 8.3 Service Invocation Security
- Dapr enforces service-to-service authorization
- Can be extended with Dapr access control policies

## 9. Acceptance Tests

### 9.1 Infrastructure Tests
- Verify Redpanda deployments are running and healthy
- Verify Dapr sidecar containers are present in backend pod
- Verify Dapr sidecar containers are present in frontend pod
- Verify Dapr components (pubsub) are installed

### 9.2 Event Publishing Tests
- Verify task creation publishes event to Redpanda
- Verify event contains correct payload schema
- Verify event publishing does not block task creation
- Verify event publishing failures are logged

### 9.3 Event Subscription Tests
- Verify backend endpoint receives events from Dapr
- Verify events are logged with proper metadata
- Verifyorten endpoint returns 200 OK for valid events
- Verify malformed events are rejected with 4xx error

### 9.4 Service Invocation Tests
- Verify frontend can call backend via Dapr
- Verify path mapping is correct for all API endpoints
- Verify authentication passes through Dapr invocation
- Verify error responses return correctly

### 9.5 Integration Tests
- Verify end-to-end flow: through event system
- Verify multiple sequential events are processed
- Verify service invocation works for CRUD operations

## 10. Out of Scope

- Complex event routing patterns (content-based routing)
- Event replay or message offset management
- Exactly-once semantics beyond Dapr defaults
- Horizontal scaling of Redpanda (multi-broker)
- Advanced Dapr features (state management, Actors, bindings beyond Pub/Sub)
- Production-grade security (mTLS external, advanced RBAC)