---
description: "Task list for Kubernetes deployment of Hackathon Todo App"
---

# Tasks: Kubernetes Deployment

**Input**: Design documents from `/specs/phase-iv-kubernetes/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/`, `frontend/`, `deploy/`
- Paths shown below assume the structure from the plan.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan
- [X] T002 Create backend/Dockerfile following multi-stage build pattern
- [X] T003 Create frontend/Dockerfile following multi-stage build pattern
- [X] T004 [P] Initialize Helm chart in deploy/k8s/helm/todo-app/

---
## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Create Chart.yaml for Helm chart in deploy/k8s/helm/todo-app/Chart.yaml
- [X] T006 Create values.yaml with default configuration in deploy/k8s/helm/todo-app/values.yaml
- [X] T007 Create templates/ directory in deploy/k8s/helm/todo-app/
- [X] T008 [P] Create postgres-statefulset.yaml in deploy/k8s/helm/todo-app/templates/postgres-statefulset.yaml
- [X] T009 [P] Create postgres-service.yaml in deploy/k8s/helm/todo-app/templates/postgres-service.yaml
- [X] T010 [P] Create backend-deployment.yaml in deploy/k8s/helm/todo-app/templates/backend-deployment.yaml
- [X] T011 [P] Create backend-service.yaml in deploy/k8s/helm/todo-app/templates/backend-service.yaml
- [X] T012 [P] Create frontend-deployment.yaml in deploy/k8s/helm/todo-app/templates/frontend-deployment.yaml
- [X] T013 [P] Create frontend-service.yaml in deploy/k8s/helm/todo-app/templates/frontend-service.yaml
- [X] T014 [P] Create secrets.yaml in deploy/k8s/helm/todo-app/templates/secrets.yaml
- [X] T015 Create deployment script in deploy/local-setup.sh

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Deploy Application Stack (Priority: P1) 🎯 MVP

**Goal**: Deploy the entire Hackathon Todo App stack to a local Kubernetes cluster using Helm so that developers can test the application in a production-like environment.

**Independent Test**: Can be fully tested by running `helm install` command and verifying that all services are running and accessible, delivering a complete working application.

### Implementation for User Story 1

- [ ] T016 [P] [US1] Update backend/Dockerfile to implement multi-stage build with Python 3.12-slim
- [ ] T017 [P] [US1] Update frontend/Dockerfile to implement multi-stage build with Node 20-alpine
- [ ] T018 [US1] Configure postgres-statefulset.yaml with PersistentVolumeClaim for data persistence
- [ ] T019 [US1] Configure postgres-service.yaml with ClusterIP for internal access
- [ ] T020 [US1] Configure backend-deployment.yaml with proper environment variables
- [ ] T021 [US1] Configure backend-service.yaml with ClusterIP for internal access
- [ ] T022 [US1] Configure frontend-deployment.yaml with NEXT_PUBLIC_API_URL environment variable
- [ ] T023 [US1] Configure frontend-service.yaml with NodePort for external access
- [ ] T024 [US1] Configure secrets.yaml with sensitive configuration (GEMINI_API_KEY, SECRET_KEY, DB password)
- [ ] T025 [US1] Implement deploy/local-setup.sh with commands to start Minikube and switch Docker context
- [ ] T026 [US1] Add image build commands to deploy/local-setup.sh
- [ ] T027 [US1] Add Helm install command to deploy/local-setup.sh

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Build Container Images (Priority: P2)

**Goal**: Build optimized container images for the frontend and backend components so that developers can deploy lightweight and secure containers to Kubernetes.

**Independent Test**: Can be fully tested by running `docker build` commands for both frontend and backend and verifying successful image creation with appropriate base images and configurations.

### Implementation for User Story 2

- [ ] T028 [P] [US2] Enhance backend/Dockerfile with uv dependency management
- [ ] T029 [P] [US2] Optimize backend/Dockerfile for size reduction
- [ ] T030 [P] [US2] Enhance frontend/Dockerfile with Next.js standalone build
- [ ] T031 [US2] Optimize frontend/Dockerfile for size reduction
- [ ] T032 [US2] Test docker build command: `docker build -t todo-backend ./backend`
- [ ] T033 [US2] Test docker build command: `docker build -t todo-frontend ./frontend`
- [ ] T034 [US2] Document Docker build process in quickstart guide

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Persist Database Data (Priority: P3)

**Goal**: Ensure the database persists data across pod restarts so that application data is not lost when Kubernetes deployments are updated or pods are restarted.

**Independent Test**: Can be verified by inserting data into the database, restarting the database pod, and confirming the data remains intact.

### Implementation for User Story 3

- [ ] T035 [P] [US3] Configure PostgreSQL StatefulSet with PersistentVolumeClaim in deploy/k8s/helm/todo-app/templates/postgres-statefulset.yaml
- [ ] T036 [US3] Configure proper storage size (1GB) in values.yaml
- [ ] T037 [US3] Test data persistence by inserting data and restarting the database pod
- [ ] T038 [US3] Verify PVC binding and storage allocation
- [ ] T039 [US3] Document persistence configuration in quickstart guide

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Verification & Testing

**Goal**: Verify the complete deployment works as expected with all functionality operational.

**Independent Test**: Verify the application stack deploys correctly, services communicate properly, and all features (including chatbot) work in the deployed version.

### Implementation for Verification

- [ ] T040 [P] Set up port forwarding to access services from host
- [ ] T041 Test pod status to ensure all services are running
- [ ] T042 [P] Check logs for backend, frontend, and database services
- [ ] T043 Verify connectivity by accessing the application at localhost:3000
- [ ] T044 Test login functionality in the deployed application
- [ ] T045 Test chatbot functionality in the deployed application
- [ ] T046 Test task creation and management in the deployed application
- [ ] T047 Validate database connectivity from backend service
- [ ] T048 Verify inter-service communication within the cluster

**Checkpoint**: Complete deployment validated and all functionality confirmed

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T049 [P] Documentation updates in deploy/README.md
- [ ] T050 Update quickstart guide with complete deployment process
- [ ] T051 Code cleanup and refactoring of Kubernetes manifests
- [ ] T052 [P] Security hardening of Kubernetes configurations
- [ ] T053 Run complete deployment validation from quickstart.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Verification (Phase 6)**: Depends on all user stories being complete
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all Dockerfile updates together:
Task: "Update backend/Dockerfile to implement multi-stage build with Python 3.12-slim"
Task: "Update frontend/Dockerfile to implement multi-stage build with Node 20-alpine"

# Launch all template updates together:
Task: "Configure postgres-statefulset.yaml with PersistentVolumeClaim for data persistence"
Task: "Configure postgres-service.yaml with ClusterIP for internal access"
Task: "Configure backend-deployment.yaml with proper environment variables"
Task: "Configure backend-service.yaml with ClusterIP for internal access"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence