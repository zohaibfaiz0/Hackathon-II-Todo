# Implementation Plan: Event-Driven Architecture with Dapr & Redpanda

**Branch**: `phase-v-cloud` | **Date**: 2026-02-08 | **Spec**: specs/phase-v-cloud/spec.md

## Summary

Extend the Kubernetes-deployed Hackathon Todo App with an event-driven architecture using Dapr sidecars and Redpanda (Kafka-compatible) for pub/sub messaging. This involves adding Redpanda as a Helm chart dependency, configuring Dapr components for Pub/Sub and Service Invocation, annotating existing Kubernetes deployments for Dapr sidecar injection, and implementing event publishing and subscription logic in the backend service.

## Technical Context

**Language/Version**: Python 3.12+ (backend), Node 20+ / Next.js 16+ (frontend)
**Primary Dependencies**: Dapr 1.14+, Redpanda 25.2+, Helm 3.x, Kubernetes 1.28+
**Event Bus**: Redpanda (Kafka-compatible distributed log)
**Runtime**: Dapr sidecars injected via Dapr Injector in Kubernetes
**Testing**: Manual verification of event publishing, subscription, and service invocation
**Target Platform**: Minikube local Kubernetes cluster (extends Phase 4 deployment)
**Project Type**: Event-driven web application with microservices communication
**Performance Goals**: Event publishing < 100ms, service invocation overhead < 10ms
**Constraints**: Non-blocking event publishing, seamless frontend/backend communication via Dapr
**Scale/Scope**: Local development with single Redpanda broker, supports future horizontal scaling

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

1. **Layer Architecture Compliance**: The event-driven enhancement maintains the existing layered architecture (Presentation: Next.js frontend, Application: FastAPI with event publishing, Infrastructure: PostgreSQL + Redpanda). Dapr sidecars act as cross-cutting infrastructure without violating layer boundaries.
2. **Technology Approval**: Redpanda and Dapr are approved for this phase as standard cloud-native event-driven patterns.
3. **Security Requirements**: Dapr's built-in mTLS will be used for service-to-service communication, and RBAC will be properly configured for Dapr components.
4. **No Manual Code**: All Dapr configurations, event schemas, and service invocation patterns will follow the spec requirements.

## Project Structure

### Documentation (this feature)
```text
specs/phase-v-cloud/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (optional - if needed)
├── data-model.md        # Phase 1 output (optional - if needed)
├── quickstart.md        # Phase 1 output (optional - if needed)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Helm Chart Extensions (existing)
```text
deploy/k8s/helm/todo-app/
├── Chart.yaml           # MODIFIED: Add Redpanda dependency
├── values.yaml          # MODIFIED: Add Redpanda and Dapr config
└── templates/
    ├── backend-deployment.yaml    # MODIFIED: Add Dapr annotations
    ├── frontend-deployment.yaml   # MODIFIED: Add Dapr annotations
    ├── dapr-pubsub-component.yaml         # NEW: Pub/Sub component for Redpanda
    ├── dapr-subscription-component.yaml   # NEW: Subscription for task events
    └── dapr-config-map.yaml               # NEW: Dapr configuration
```

### Source Code (repository root)
```text
hackathon-todo/
├── backend/
│   └── src/
│       └── hackathon_todo_api/
│           ├── main.py                  # MODIFIED: Add event publishing
│           ├── models/
│           │   └── task.py              # MODIFIED: Add event publishing on create
│           ├── events/                  # NEW
│           │   ├── publisher.py         # NEW: Dapr event publishing
│           │   └── subscriber.py        # NEW: Event subscription endpoint
│           └── requirements.txt         # MODIFIED: Add httpx
└── frontend/
    └── src/
        └── lib/
            └── api.ts                   # MODIFIED: Use Dapr Service Invocation
```

**Structure Decision**: The existing Phase 4 structure will be extended. Helm chart will be modified to include Redpanda dependency and Dapr components. Backend will have a new `events/` module for event-related functionality. Frontend API client will be updated to use Dapr invocation pattern.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Dapr sidecar injection | Required for Pub/Sub and Service Invocation capabilities without code changes | Direct Kafka client would require more boilerplate and lack built-in service discovery |
| Event publishing in task creation | Enables decoupled architecture for future consumers | Synchronous logging is simpler but doesn't enable event-driven extensibility |

## Phase 0: Research

**Dapr Setup Requirements**:
- Dapr must be installed on the Kubernetes cluster before deploying the application
- Use `helm repo add` and `helm install dapr dapr/dapr` for initial setup
- Dapr Injector component required for sidecar injection via annotations

**Redpanda Chart Options**:
- Chart source: `charts.redpanda.com/redpanda`
- Minimal configuration: single replica for local development
- Persistence: 10Gi default storage

**Dapr Component Configuration**:
- Pub/Sub type: `pubsub.redpanda`
- Requires Redpanda bootstrap server address from cluster service

## Phase 1: Design - Data Model

### Event Data Model

**CloudEvents Standard Schema**:
- `id`: unique event identifier (UUID)
- `source`: event source service identifier
- `type`: event type identifier (e.g., `task.created`)
- `specversion`: CloudEvents spec version (1.0)
- `time`: event timestamp (ISO 8601)
- `datacontenttype`: content type of data payload
- `data`: event-specific payload

**TaskCreatedEvent**:
```python
class TaskCreatedEvent(BaseModel):
    task_id: uuid.UUID
    user_id: uuid.UUID
    title: str
    description: str | None = None
    completed: bool
    created_at: datetime
```

## Phase 1: Design - Interfaces

### Internal Interfaces

**EventPublisher**:
```python
class EventPublisher:
    async def publish_event(self, topic: str, event_type: str, data: dict) -> None
        # Publishes event to Dapr Pub/Sub
```

**EventSubscriberEndpoint**:
```python
@app.post("/api/events/task-created")
async def handle_task_created_event(cloudevent: CloudEvent) -> JSONResponse:
    # Handles incoming event from Dapr
```

### External Interfaces

**Dapr Pub/Sub API**:
- Endpoint: `http://localhost:3500/v1.0/publish/{pubsub}/{topic}`
- Method: POST
- Headers: `Content-Type: application/cloudevents+json`

**Dapr Service Invocation API**:
- Endpoint: `http://localhost:3500/v1.0/invoke/{appId}/method/{method}`
- Method: Mirrors client request (GET/POST/PATCH/DELETE)
- Headers: Passed through to target service

## Phase 1: Design - NFRs and Budgets

### Performance
- Event publishing latency: < 100ms (p95)
- Dapr service invocation overhead: < 10ms (p95)
- Event processing (subscription): < 50ms (p95)
- Total impact on task creation: < 150ms additional latency

### Reliability
- Event delivery: At-least-once (via Dapr Pub/Sub)
- Service invocation retries: 3 retries with exponential backoff (Dapr default)
- Event acknowledgment: 200 OK from subscription endpoint

### Security
- Inter-service communication: mTLS (Dapr default)
- Event content: User-scoped data, no credentials
- RBAC: Kubernetes native for component access

### Cost (Local Development)
- Redpanda storage: 10Gi default
- Dapr sidecar memory: ~64MB per pod
- Additional network traffic: Event payloads only

### Data Management

**Event Retention**:
- Redpanda default retention: 7 days (configurable via Helm values)
- No offset management required for basic pub/sub

**Schema Evolution**:
- Events follow CloudEvents standard for extensibility
- Backward-compatible data changes allowed within data field

## Phase 1: Design - Operational Readiness

### Observability
- **Logs**: Backend logs event publishing attempts and subscription processing
- **Metrics**: Dapr provides built-in metrics for Pub/Sub and Service Invocation
- **Traces**: Distributed tracing available via Dapr OTel (optional)

### Runbooks
- **Deploy**: Deploy Dapr, then deploy application chart (includes Redpanda)
- **Verify Events**: Check backend logs for event publishing/consumption
- **Troubleshoot Events**: Use Dapr CLI: `dapr logs` and `dapr status`
- **Troubleshoot Service Invocation**: Verify Dapr sidecar status and log connections

### Deployment Strategy
- Existing Helm chart extended with new components
- No breaking changes to existing deployments (annotations additive)
- Rolling update supported via Kubernetes Deployment

### Alerting (Local Development)
- No alerting configured for local development
- Dapr logs provide operational feedback

## Phase 1: Design - Risk Analysis

### Top 3 Risks

| Risk | Blast Radius | Mitigation |
|------|--------------|------------|
| Dapr cluster not installed | Application deployment fails | Document prerequisite: `helm install dapr` before app deployment |
| Redpanda compatibility | Event publishing/subscription fails | Use stable Redpanda chart version; test components separately |
| Dapr sidecar injection failure | App pods start without Dapr | Validate annotations and Dapr Injector status; check pod sidecar containers |

## Phase 2: Tasks Overview

The implementation is organized around three main areas:

1. **Infrastructure (T-501 to T-504)**: Helm chart modifications and Dapr components
2. **Backend Code (T-505 to T-506)**: Event publishing and subscription logic
3. **Frontend Code (T-507)**: Service Invocation pattern for API calls

All tasks are atomic and independently testable.

## Implementation Strategy

### Incremental Delivery

1. **Infrastructure First**: Deploy Redpanda and Dapr components independently
2. **Event Publishing**: Add event publishing to backend, verify events reach Redpanda
3. **Event Subscription**: Add subscription endpoint, verify events are consumed
4. **Service Invocation**: Update frontend to use Dapr, verify API calls work
5. **Integration**: End-to-end verification of event-driven flow

### Parallel Opportunities

- Infrastructure tasks (T-501 to T-504) can be done in parallel
- Backend event publishing (T-505) and subscription (T-506) are independent
- Frontend service invocation (T-507) depends on backend being Dapr-enabled but not on events

## Key Architectural Decisions

### Decision 1: Use Dapr for Pub/Sub vs Direct Kafka Client

**Chosen**: Dapr Pub/Sub with Redpanda component

**Rationale**:
- Consistent abstraction layer for service discovery
- Built-in retries, timeouts, and observability
- Sidecar pattern keeps application code clean
- Easier testing with Dapr CLI locally

### Decision 2: Event Publishing on Task Creation Only

**Chosen**: Fire-and-forget publishing only for `task.created` eventsany

**Rationale**:
- Phase 5 is introductory event-driven implementation
- Update/delete events can be added in future phases
- Focus on core event-driven pattern before expanding scope

### Decision 3: Service Invocation via Dapr for All Frontend Calls

**Chosen**: Update all frontend API calls to use Dapr invocation

**Rationale**:
- Consistent service discovery and resilience
- Enables future features like retries, timeouts, observability
- Single pattern to maintain

### Decision 4: Non-Blocking Event Publishing

**Chosen**: Publish event without waiting for confirmation/ retry

**Rationale**:
- Event publishing failure shouldn't affect user experience
- Dapr provides at-least-once guarantees internally
- Logging sufficient for debugging in development phase

## Dependencies & Execution Order

1. **Foundation**: Helm chart modifications (T-501 to T-504)
2. **Backend**: Event publishing (T-505) → Event subscription (T-506)
3. **Frontend**: Service Invocation (T-507)
4. **Verification**: Integration testing and documentation

## Testing Strategy

- Unit tests (optional): Event publisher and subscriber logic
- Integration tests: Manual verification of event flow
- End-to-end tests: Task creation → event → API call via Dapr

## Definition of Done

- [ ] All infrastructure tasks complete and verified
- [ ] Backend publishes events on task creation
- [ ] Backend subscribes to and logs events
- [ ] Frontend calls backend via Dapr Service Invocation
- [ ] All user stories acceptance criteria met
- [ ] Documentation updated
- [ ] Clean commit history per task/feature