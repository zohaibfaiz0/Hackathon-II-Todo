---
description: "Task list for Event-Driven Architecture with Dapr & Redpanda"
---

# Tasks: Event-Driven Architecture with Dapr & Redpanda

**Input**: Design documents from `/specs/phase-v-cloud/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: Manual verification of event publishing, subscription, and service invocation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US-501, US-502, US-503)
- Include exact file paths in descriptions

## Path Conventions

- **Helm Chart**: `deploy/k8s/helm/todo-app/`
- **Backend**: `backend/src/hackathon_todo_api/`
- **Frontend**: `frontend/src/lib/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prerequisites and initial configuration

- [ ] T-500 Create prerequisite documentation for Dapr cluster installation
  - Document `helm repo add dapr https://dapr.github.io/helm-charts/`
  - Document `helm install --namespace dapr-system --create-namespace dapr dapr/dapr`
  - Document `dapr init -k` for local CLI setup

---

## Phase 2: Foundational (Infrastructure)

**Purpose**: Helm chart modifications and Dapr components - blocks all user stories

**⚠️ CRITICAL**: No user story code changes can begin until this phase is complete

- [ ] T-501 [P] [US-501] Add Redpanda dependency to Chart.yaml
  - Modify `deploy/k8s/helm/todo-app/Chart.yaml`
  - Add dependency: name `redpanda`, version `25.2.x` or latest, repository `https://charts.redpanda.com`
  - Set condition `redpanda.enabled`

- [ ] T-502 [P] [US-501] Add Redpanda configuration to values.yaml
  - Modify `deploy/k8s/helm/todo-app/values.yaml`
  - Configure Redpanda statefulset: single replica, 10Gi storage, default memory limits
  - Configure Redpanda service: cluster IP, bootstrap server info

- [ ] T-503 [P] [US-501] Create Dapr Pub/Sub component template (dapr-pubsub-component.yaml)
  - Create `deploy/k8s/helm/todo-app/templates/dapr-pubsub-component.yaml`
  - Define kind: Component, apiVersion: dapr.io/v1alpha1
  - Set type: pubsub.redpanda, name: todo-pubsub
  - Configure metadata: topics array with 'tasks', bootstrapServers from Redpanda service

- [ ] T-504 [P] [US-502] Create Dapr Subscription component template (dapr-subscription-component.yaml)
  - Create `deploy/k8s/helm/todo-app/templates/dapr-subscription-component.yaml`
  - Define kind: Subscription, apiVersion: dapr.io/v1alpha1
  - Set pubsubname: todo-pubsub, topic: tasks
  - Set route: /api/events/task-created
  - Set metadata: deadLetterTopic (optional)

- [ ] T-505 [P] [US-503] Add Dapr annotations to backend deployment
  - Modify `deploy/k8s/helm/todo-app/templates/backend-deployment.yaml`
  - Add dapr.io/enabled: "true" annotation to pod template
  - Add dapr.io/app-id: "backend" annotation
  - Add dapr.io/app-port: "8000" annotation (backend port)
  - Optionally add dapr.io/log-level: "info"

- [ ] T-506 [P] [US-503] Add Dapr annotations to frontend deployment
  - Modify `deploy/k8s/helm/todo-app/templates/frontend-deployment.yaml`
  - Add dapr.io/enabled: "true" annotation to pod template
  - Add dapr.io/app-id: "frontend" annotation
  - Add dapr.io/app-port: "3000" annotation (frontend port)
  - Optionally add dapr.io/log-level: "info"

**Checkpoint**: Infrastructure ready - user story implementation can now begin

---

## Phase 3: User Story 501 - Publish Task Creation Events (Priority: P1) 🎯 MVP

**Goal**: Backend publishes `task.created` event when tasks are created.

**Independent Test**: Can be tested by creating a task and verifying event appears in Redpanda topic.

### Implementation for User Story 501

- [ ] T-507 [P] [US-501] Add httpx dependency to backend requirements
  - Modify `backend/src/hackathon_todo_api/requirements.txt`
  - Add `httpx` line for async HTTP client
  - Optionally add `pydantic` if not already present for CloudEvents

- [ ] T-508 [US-501] Create events directory in backend
  - Create `backend/src/hackathon_todo_api/events/`
  - Create `backend/src/hackathon_todo_api/events/__init__.py` (empty or with exports)

- [ ] T-509 [US-501] Create CloudEvent data model
  - Create `backend/src/hackathon_todo_api/events/models.py`
  - Define `CloudEvent` Pydantic model with: id, source, type, specversion, time, datacontenttype, data
  - Define `TaskCreatedEvent` Pydantic model with: task_id, user_id, title, description, completed, created_at

- [ ] T-510 [US-501] Create EventPublisher class
  - Create `backend/src/hackathon_todo_api/events/publisher.py`
  - Define `EventPublisher` class with async `publish_event()` method
  - Implement Dapr HTTP API call to `http://localhost:3500/v1.0/publish/todo-pubsub/tasks`
  - Format event as CloudEvents with proper headers and body
  - Implement fire-and-forget pattern: fire request, log result, no await or retry

- [ ] T-511 [US-501] Integrate event publishing into task creation
  - Modify `backend/src/hackathon_todo_api/routes/tasks.py` (or equivalent)
  - Import `EventPublisher` and `TaskCreatedEvent`
  - After database insert and before response, publish `task.created` event
  - Use fire-and-forget pattern: create task, spawn event publish, return response
  - Log event publishing success/failure without blocking

- [ ] T-512 [US-501] Test event publishing locally
  - Deploy application with updated chart
  - Create a task via API or UI
  - Check backend logs for event publishing confirmation
  - Verify event published to Redpanda topic (use kubectl or Redpanda CLI)

**Checkpoint**: At this point, User Story 501 should be fully functional and testable independently

---

## Phase 4: User Story 502 - Consume Task Creation Events (Priority: P2)

**Goal**: Backend subscribes to `task.created` events and logs them.

**Independent Test**: Can be tested by creating a task and verifying event appears in backend logs.

### Implementation for User Story 502

- [ ] T-513 [P] [US-502] Create event subscription module
  - Create `backend/src/hackathon_todo_api/events/subscriber.py`
  - Define `CloudEventRequest` model for incoming Dapr events
  - Create validation logic for `task.created` event type
  - Implement logging with timestamp, event ID, and data

- [ ] T-514 [US-502] Add event subscription endpoint to main router
  - Modify `backend/src/hackathon_todo_api/main.py`
  - Add POST route `/api/events/task-created`
  - Import and use event subscription handler from subscriber module
  - Validate incoming CloudEvent format
  - Log event details and return 200 OK

- [ ] T-515 [US-502] Test event subscription
  - Deploy application with subscription endpoint
  - Create a task to trigger event publishing
  - Check backend logs for event subscription confirmation
  - Verify `/api/events/task-created` endpoint is called by Dapr

**Checkpoint**: At this point, User Stories 501 AND 502 should both work independently

---

## Phase 5: User Story 503 - Invoke Backend via Dapr Service Invocation (Priority: P2)

**Goal**: Frontend calls backend APIs via Dapr sidecar.

**Independent Test**: Can be tested by accessing the frontend and verifying all functionality works.

### Implementation for User Story 503

- [ ] T-516 [P] [US-503] Update frontend API client base configuration
  - Modify `frontend/src/lib/api.ts` (or equivalent)
  - Add conditional config: use Dapr if `DAPR_ENABLED` environment variable is true
  - Set Dapr base URL: `http://localhost:3500/v1.0/invoke/backend/method/`
  - Set direct HTTP base URL as fallback

- [ ] T-517 [US-503] Update fetch wrapper for Dapr Service Invocation
  - Modify `frontend/src/lib/api.ts`
  - Update `apiFetch` function to strip leading `/` before appending to Dapr base URL
  - Preserve query parameters, body, and method from original request
  - Update path mapping: `/api/tasks` → `api/tasks` relative to Dapr method path

- [ ] T-518 [US-503] Update authentication calls for Dapr
  - Modify `frontend/src/lib/auth.ts` (or equivalent login/signup functions)
  - Ensure `/api/auth/login` and `/api/auth/register` calls use updated apiFetch
  - Test authentication works via Dapr invocation

- [ ] T-519 [US-503] Update all task CRUD calls for Dapr
  - Modify all frontend components calling API (`apps/tasks/page.tsx`, etc.)
  - Verify following API calls use updated apiFetch:
    - `GET /api/tasks`
    - `POST /api/tasks`
    - `PUT /api/tasks/{id}`
    - `DELETE /api/tasks/{id}`
    - `PATCH /api/tasks/{id}/toggle-complete`

- [ ] T-520 [US-503] Test service invocation end-to-end
  - Enable Dapr via environment variable
  - Access frontend UI
  - Test login functionality
  - Test task creation, update, delete, toggle
  - Verify all operations work via Dapr

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Verification & Testing

**Goal**: Verify the complete event-driven architecture works as expected.

### Implementation for Verification

- [ ] T-521 [P] Verify Dapr cluster installation
  - Run `kubectl get pods -n dapr-system` to verify Dapr components are running
  - Check `dapr status` CLI output

- [ ] T-522 [P] Verify Redpanda deployment
  - Run `kubectl get statefulsets` to verify Redpanda is deployed
  - Check `kubectl get pods` for redpanda pods
  - Verify Redpanda service is accessible within cluster

- [ ] T-523 [P] Verify Dapr sidecar injection
  - Run `kubectl get pods` to check app pods
  - Describe pods to verify sidecar containers are present
  - Check pod status for both app and sidecar containers

- [ ] T-524 [P] Verify Dapr components installation
  - Run `kubectl get components` to verify Pub/Sub component is installed
  - Run `kubectl get components` to verify Subscription component is installed
  - Check component configuration with `kubectl describe component`

- [ ] T-525 Test event publishing flow
  - Create a task via frontend or API
  - Check backend logs for event publishing confirmation
  - Verify event in Redpanda topic (use CLI or consumer)

- [ ] T-526 Test event subscription flow
  - Create a task
  - Check backend logs for event subscription confirmation
  - Verify event was logged with correct metadata

- [ ] T-527 Test service invocation for authentication
  - Attempt login via frontend
  - Verify successful authentication via Dapr invocation
  - Check frontend and backend logs for invocation confirmation

- [ ] T-528 Test service invocation for task operations
  - Create, update, delete, and complete tasks
  - Verify all operations work via Dapr invocation
  - Check logs for invocation traces

- [ ] T-529 Test end-to-end event-driven flow
  - Create task → event published → event consumed → logged
  - Verify complete flow works without errors
  - Check logs end-to-end

**Checkpoint**: Complete event-driven architecture validated

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Documentation and cleanup

- [ ] T-530 [P] Update deployment documentation
  - Modify `deploy/README.md` or create new Dapr-specific docs
  - Document Dapr prerequisite installation steps
  - Document deployment steps for Phase 5
  - Include troubleshooting section

- [ ] T-531 Update quickstart guide
  - Modify `deploy/QUICKSTART.md` or create new guide
  - Add Phase 5 setup instructions
  - Include Dapr and Redpanda configuration notes
  - Add verification steps

- [ ] T-532 Create Dapr troubleshooting guide
  - Create `deploy/TROUBLESHOOTING-DAPR.md`
  - Common issues and solutions
  - Dapr CLI commands for debugging
  - Kubernetes validation steps

- [ ] T-533 [P] Code cleanup and refactoring
  - Review event publishing code for improvements
  - Review service invocation code for patterns
  - Remove any debugging code
  - Ensure TypeScript/Python types are correct

- [ ] T-534 Update Helm chart README
  - Update `deploy/k8s/helm/todo-app/README.md`
  - Document new Redpanda configuration options
  - Document Dapr configuration options
  - Include upgrade instructions from Phase 4

**Checkpoint**: Complete feature ready for deployment and documentation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - should be documented before deployment
- **Foundational (Phase 2并发)**: BLOCKS all user stories - infrastructure must be ready first
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
- **Verification (Phase 6)**: Depends on all user stories being complete
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 501 (P1)**: Depends on Foundational - no dependencies on other stories
- **User Story 502 (P2)**: Depends on Foundational - independent of US-501
- **User Story 503 (P2)**: Depends on Foundational and backend being Dapr-enabled (from Foundational phase) - independent of event stories

### Within Each User Story

- Models before publishers/subscribers
- Publishers before integration points
- Integration before subscription endpoints
- Configuration updates before code changes

### Parallel Opportunities

- All Foundational tasks marked [P] can run in parallel
- US-501 tasks: T-507 [P] and T-508/T-509 have some dependencies
- US-502 task T-513 [P] is independent and can be done in parallel
- US-503 tasks: T-516 and T-517 are [P] and can run in parallel

---

## Parallel Example: Foundational Phase

```bash
# All of these can be launched in parallel:
Task: "Add Redpanda dependency to Chart.yaml" (T-501)
Task: "Add Redpanda configuration to values.yaml" (T-502)
Task: "Create Dapr Pub/Sub component template" (T-503)
Task: "Create Dapr Subscription component template" (T-504)
Task: "Add Dapr annotations to backend deployment" (T-505)
Task: "Add Dapr annotations to frontend deployment" (T-506)
```

---

## Implementation Strategy

### MVP First (User Story 501 Only)

1. Complete Phase 1: Setup (documentation)
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 501
4. **STOP and VALIDATE**: Test event publishing independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Infrastructure ready
2. Add US-501 → Test independently → Validate event publishing
3. Add US-502 → Test independently → Validate event subscription
4. Add US-503 → Test independently → Validate service invocation
5. Each story adds event-driven capabilities without breaking existing functionality

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 501 (event publishing)
   - Developer B: User Story 502 (event subscription)
   - Developer C: User Story 503 (service invocation)
3. Stories complete and verify independently
4. Team integration and end-to-end testing

---

## Notes

- [P] tasks = different files, no dependencies
- [US-XXX] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies
- Dapr must be installed on cluster before deploying application chart (prerequisite)
- Event publishing is fire-and-forget (non-blocking to main flow)
- Service invocation is transparent pattern change for frontend