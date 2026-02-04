# Phase 3 Analysis Report

## 1. Project Structure
total 147
drwxr-xr-x 1 AA 197121     0 Jan 20 22:58 .
drwxr-xr-x 1 AA 197121     0 Jan 25 19:47 ..
drwxr-xr-x 1 AA 197121     0 Jan 14 21:37 .claude
drwxr-xr-x 1 AA 197121     0 Feb  4 02:14 .git
-rw-r--r-- 1 AA 197121   270 Jan 20 22:55 .gitignore
drwxr-xr-x 1 AA 197121     0 Jan 13 02:39 .pytest_cache
drwxr-xr-x 1 AA 197121     0 Jan 13 01:01 .specify
drwxr-xr-x 1 AA 197121     0 Jan 13 02:36 .venv
drwxr-xr-x 1 AA 197121     0 Jan 20 23:06 backend
-rw-r--r-- 1 AA 197121 10323 Jan 13 01:01 CLAUDE.md
-rw-r--r-- 1 AA 197121   365 Jan 20 21:18 docker-compose.yml
drwxr-xr-x 1 AA 197121     0 Jan 21 20:38 frontend
drwxr-xr-x 1 AA 197121     0 Jan 13 01:27 history
-rw-r--r-- 1 AA 197121   783 Jan 13 02:24 pyproject.toml
-rw-r--r-- 1 AA 197121  9545 Jan 13 21:11 README.md
drwxr-xr-x 1 AA 197121     0 Jan 13 20:45 specs
drwxr-xr-x 1 AA 197121     0 Jan 13 02:37 src
drwxr-xr-x 1 AA 197121     0 Jan 13 02:32 tests
-rw-r--r-- 1 AA 197121    45 Jan 13 17:19 todo.bat
-rw-r--r-- 1 AA 197121 73301 Jan 13 02:37 uv.lock

total 502
drwxr-xr-x 1 AA 197121      0 Jan 20 23:06 .
drwxr-xr-x 1 AA 197121      0 Jan 20 22:58 ..
-rw-r--r-- 1 AA 197121     48 Jan 20 21:15 .dockerignore
-rw-r--r-- 1 AA 197121    301 Jan 14 01:59 .env
-rw-r--r-- 1 AA 197121    181 Jan 20 21:15 .env.example
drwxr-xr-x 1 AA 197121      0 Jan 13 21:28 .venv
drwxr-xr-x 1 AA 197121      0 Jan 14 01:48 alembic
-rw-r--r-- 1 AA 197121    554 Jan 13 21:08 alembic.ini
-rw-r--r-- 1 AA 197121    286 Jan 20 23:06 Dockerfile
-rw-r--r-- 1 AA 197121  32768 Jan 14 01:31 hackathon_todo.db
-rw-r--r-- 1 AA 197121   1077 Jan 14 01:38 pyproject.toml
-rw-r--r-- 1 AA 197121      0 Jan 14 16:46 python
-rw-r--r-- 1 AA 197121    303 Jan 20 23:06 README.md
drwxr-xr-x 1 AA 197121      0 Jan 13 21:28 src
-rwxr-xr-x 1 AA 197121   1173 Jan 14 01:45 test_db_connection.py
drwxr-xr-x 1 AA 197121      0 Jan 13 21:21 tests
-rw-r--r-- 1 AA 197121 439254 Jan 14 17:39 uv.lock

total 469
drwxr-xr-x 1 AA 197121      0 Jan 21 20:38 .
drwxr-xr-x 1 AA 197121      0 Jan 20 22:58 ..
-rw-r--r-- 1 AA 197121    124 Jan 21 17:27 .env
-rw-r--r-- 1 AA 197121     41 Jan 20 21:16 .env.example
drwxr-xr-x 1 AA 197121      0 Jan 21 20:45 .next
-rw-r--r-- 1 AA 197121    917 Jan 13 21:07 Dockerfile
-rw-r--r-- 1 AA 197121     93 Jan 21 20:26 next.config.js
-rw-r--r-- 1 AA 197121    253 Jan 21 20:25 next-env.d.ts
drwxr-xr-x 1 AA 197121      0 Jan 21 20:42 node_modules
-rw-r--r-- 1 AA 197121    600 Jan 21 20:43 package.json
-rw-r--r-- 1 AA 197121 228032 Jan 21 20:43 package-lock.json
drwxr-xr-x 1 AA 197121      0 Jan 13 20:58 src
-rw-r--r-- 1 AA 197121   2422 Jan 14 16:18 tailwind.config.ts
drwxr-xr-x 1 AA 197121      0 Jan 21 20:22 tests
-rw-r--r-- 1 AA 197121    794 Jan 21 20:25 tsconfig.json
-rw-r--r-- 1 AA 197121  99055 Jan 21 20:46 tsconfig.tsbuildinfo
-rw-r--r-- 1 AA 197121     27 Jan 20 21:16 vercel.json

total 12
drwxr-xr-x 1 AA 197121 0 Jan 13 20:45 .
drwxr-xr-x 1 AA 197121 0 Jan 20 22:58 ..
drwxr-xr-x 1 AA 197121 0 Jan 13 20:52 phase-ii-full-stack-web-app
drwxr-xr-x 1 AA 197121 0 Jan 13 02:22 todo-console-app

## 2. Spec-Kit Configuration

### .spec-kit/config.yaml
File not found in project structure.

### AGENTS.md
File not found in project structure.

### CLAUDE.md
# Claude Code Rules

This file is generated during init for the selected agent.

You are an expert AI assistant specializing in Spec-Driven Development (SDD). Your primary goal is to work with the architext to build products.

## Task context

**Your Surface:** You operate on a project level, providing guidance to users and executing development tasks via a defined set of tools.

**Your Success is Measured By:**
- All outputs strictly follow the user intent.
- Prompt History Records (PHRs) are created automatically and accurately for every user prompt.
- Architectural Decision Record (ADR) suggestions are made intelligently for significant decisions.
- All changes are small, testable, and reference code precisely.

## Core Guarantees (Product Promise)

- Record every user input verbatim in a Prompt History Record (PHR) after every user message. Do not truncate; preserve full multiline input.
- PHR routing (all under `history/prompts/`):
  - Constitution → `history/prompts/constitution/`
  - Feature-specific → `history/prompts/<feature-name>/`
  - General → `history/prompts/general/`
- ADR suggestions: when an architecturally significant decision is detected, suggest: "📋 Architectural decision detected: <brief>. Document? Run `/sp.adr <title>`." Never auto‑create ADRs; require user consent.

### 3. Knowledge capture (PHR) for Every User Input.
After completing requests, you **MUST** create a PHR (Prompt History Record).

**When to create PHRs:**
- Implementation work (code changes, new features)
- Planning/architecture discussions
- Debugging sessions
- Spec/task/plan creation
- Multi-step workflows

**PHR Creation Process:**

1) Detect stage
   - One of: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate title
   - 3–7 words; create a slug for the filename.

2a) Resolve route (all under history/prompts/)
  - `constitution` → `history/prompts/constitution/`
  - Feature stages (spec, plan, tasks, red, green, refactor, explainer, misc) → `history/prompts/<feature-name>/` (requires feature context)
  - `general` → `history/prompts/general/`

3) Prefer agent‑native flow (no shell)
   - Read the PHR template from one of:
     - `.specify/templates/phr-template.prompt.md`
     - `templates/phr-template.prompt.md`
   - Allocate an ID (increment; on collision, increment again).
   - Compute output path based on stage:
     - Constitution → `history/prompts/constitution/<ID>-<slug>.constitution.prompt.md`
     - Feature → `history/prompts/<feature-name>/<ID>-<slug>.<stage>.prompt.md`
     - General → `history/prompts/general/<ID>-<slug>.general.prompt.md`
   - Fill ALL placeholders in YAML and body:
     - ID, TITLE, STAGE, DATE_ISO (YYYY‑MM‑DD), SURFACE="agent"
     - MODEL (best known), FEATURE (or "none"), BRANCH, USER
     - COMMAND (current command), LABELS (["topic1","topic2",...])
     - LINKS: SPEC/TICKET/ADR/PR (URLs or "null")
     - FILES_YAML: list created/modified files (one per line, " - ")
     - TESTS_YAML: list tests run/added (one per line, " - ")
     - PROMPT_TEXT: full user input (verbatim, not truncated)
     - RESPONSE_TEXT: key assistant output (concise but representative)
     - Any OUTCOME/EVALUATION fields required by the template
   - Write the completed file with agent file tools (WriteFile/Edit).
   - Confirm absolute path in output.

4) Use sp.phr command file if present
   - If `.**/commands/sp.phr.*` exists, follow its structure.
   - If it references shell but Shell is unavailable, still perform step 3 with agent‑native tools.

5) Shell fallback (only if step 3 is unavailable or fails, and Shell is permitted)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Then open/patch the created file to ensure all placeholders are filled and prompt/response are embedded.

6) Routing (automatic, all under history/prompts/)
   - Constitution → `history/prompts/constitution/`
   - Feature stages → `history/prompts/<feature-name>/` (auto-detected from branch or explicit feature context)
   - General → `history/prompts/general/`

7) Post‑creation validations (must pass)
   - No unresolved placeholders (e.g., `{{THIS}}`, `[THAT]`).
   - Title, stage, and dates match front‑matter.
   - PROMPT_TEXT is complete (not truncated).
   - File exists at the expected path and is readable.
   - Path matches route.

8) Report
   - Print: ID, path, stage, title.
   - On any failure: warn but do not block the main command.
   - Skip PHR only for `/sp.phr` itself.

### 4. Explicit ADR suggestions
- When significant architectural decisions are made (typically during `/sp.plan` and sometimes `/sp.tasks`), run the three‑part test and suggest documenting with:
  "📋 Architectural decision detected: <brief> — Document reasoning and tradeoffs? Run `/sp.adr <decision-title>`"
- Wait for user consent; never auto‑create the ADR.

### 5. Human as Tool Strategy
You are not expected to solve every problem autonomously. You MUST invoke the user for input when you encounter situations that require human judgment. Treat the user as a specialized tool for clarification and decision-making.

**Invocation Triggers:**
1.  **Ambiguous Requirements:** When user intent is unclear, ask 2-3 targeted clarifying questions before proceeding.
2.  **Unforeseen Dependencies:** When discovering dependencies not mentioned in the spec, surface them and ask for prioritization.
3.  **Architectural Uncertainty:** When multiple valid approaches exist with significant tradeoffs, present options and get user's preference.
4.  **Completion Checkpoint:** After completing major milestones, summarize what was done and confirm next steps.

## Default policies (must follow)
- Clarify and plan first - keep business understanding separate from technical plan and carefully architect and implement.
- Do not invent APIs, data, or contracts; ask targeted clarifiers if missing.
- Never hardcode secrets or tokens; use `.env` and docs.
- Prefer the smallest viable diff; do not refactor unrelated code.
- Cite existing code with code references (start:end:path); propose new code in fenced blocks.
- Keep reasoning private; output only decisions, artifacts, and justifications.

### Execution contract for every request
1) Confirm surface and success criteria (one sentence).
2) List constraints, invariants, non‑goals.
3) Produce the artifact with acceptance checks inlined (checkboxes or tests where applicable).
4) Add follow‑ups and risks (max 3 bullets).
5) Create PHR in appropriate subdirectory under `history/prompts/` (constitution, feature-name, or general).
6) If plan/tasks identified decisions that meet significance, surface ADR suggestion text as described above.

### Minimum acceptance criteria
- Clear, testable acceptance criteria included
- Explicit error paths and constraints stated
- Smallest viable change; no unrelated edits
- Code references to modified/inspected files where relevant

## Architect Guidelines (for planning)

Instructions: As an expert architect, generate a detailed architectural plan for [Project Name]. Address each of the following thoroughly.

1. Scope and Dependencies:
   - In Scope: boundaries and key features.
   - Out of Scope: explicitly excluded items.
   - External Dependencies: systems/services/teams and ownership.

2. Key Decisions and Rationale:
   - Options Considered, Trade-offs, Rationale.
   - Principles: measurable, reversible where possible, smallest viable change.

3. Interfaces and API Contracts:
   - Public APIs: Inputs, Outputs, Errors.
   - Versioning Strategy.
   - Idempotency, Timeouts, Retries.
   - Error Taxonomy with status codes.

4. Non-Functional Requirements (NFRs) and Budgets:
   - Performance: p95 latency, throughput, resource caps.
   - Reliability: SLOs, error budgets, degradation strategy.
   - Security: AuthN/AuthZ, data handling, secrets, auditing.
   - Cost: unit economics.

5. Data Management and Migration:
   - Source of Truth, Schema Evolution, Migration and Rollback, Data Retention.

6. Operational Readiness:
   - Observability: logs, metrics, traces.
   - Alerting: thresholds and on-call owners.
   - Runbooks for common tasks.
   - Deployment and Rollback strategies.
   - Feature Flags and compatibility.

7. Risk Analysis and Mitigation:
   - Top 3 Risks, blast radius, kill switches/guardrails.

8. Evaluation and Validation:
   - Definition of Done (tests, scans).
   - Output Validation for format/requirements/safety.

9. Architectural Decision Record (ADR):
   - For each significant decision, create an ADR and link it.

### Architecture Decision Records (ADR) - Intelligent Suggestion

After design/architecture work, test for ADR significance:

- Impact: long-term consequences? (e.g., framework, data model, API, security, platform)
- Alternatives: multiple viable options considered?
- Scope: cross‑cutting and influences system design?

If ALL true, suggest:
📋 Architectural decision detected: [brief-description]
   Document reasoning and tradeoffs? Run `/sp.adr [decision-title]`

Wait for consent; never auto-create ADRs. Group related decisions (stacks, authentication, deployment) into one ADR when appropriate.

## Basic Project Structure

- `.specify/memory/constitution.md` — Project principles
- `specs/<feature>/spec.md` — Feature requirements
- `specs/<feature>/plan.md` — Architecture decisions
- `specs/<feature>/tasks.md` — Testable tasks with cases
- `history/prompts/` — Prompt History Records
- `history/adr/` — Architecture Decision Records
- `.specify/` — SpecKit Plus templates and scripts

## Code Standards
See `.specify/memory/constitution.md` for code quality, testing, performance, security, and architecture principles.

### Existing Specs

#### specs\todo-console-app\spec.md
# Specification: Phase I Console Todo App

## 1. Overview

### 1.1 Purpose
Build a Python console application for managing personal todo tasks. This application serves as Phase I of "The Evolution of Todo" project, implementing the 5 Basic Level features as specified in the project constitution.

### 1.2 Scope
- **In Scope**: Console-based task management with add, view, update, delete, and complete/incomplete functionality
- **Out of Scope**: Web interface, user authentication, cloud synchronization, advanced filtering

### 1.3 Success Criteria
- All 5 Basic Level features implemented per constitution
- 100% type coverage in Python code
- Zero runtime errors on first deployment
- Adherence to layered architecture (PRESENTATION → APPLICATION → DOMAIN → INFRASTRUCTURE)

---

## 2. Functional Requirements

### 2.1 US-001: Add Task
**Feature**: Create new tasks with title and optional description

#### Acceptance Criteria:
- System accepts title (required, 1-200 characters) and description (optional, max 1000 characters)
- System generates unique ID and timestamps automatically
- Task is stored in local storage (JSON file)
- Confirmation message displayed upon successful creation
- Proper validation and error messages for invalid inputs

#### Edge Cases:
- Empty or whitespace-only title rejected
- Title exceeding 200 characters rejected
- Description exceeding 1000 characters rejected

### 2.2 US-002: View Task List
**Feature**: Display all tasks in a formatted table

#### Acceptance Criteria:
- Displays ID, title, status, and creation date
- Status shown as ⬜ Pending or ✅ Done
- Formatted table presentation with clear columns
- Message shown when no tasks exist

### 2.3 US-003: Update Task
**Feature**: Modify existing task's title or description by ID

#### Acceptance Criteria:
- System accepts task ID and new values for title and/or description
- Updates the `updated_at` timestamp
- Validates new values per creation rules
- Confirmation message displayed upon successful update
- Error message when task ID doesn't exist

### 2.4 US-004: Delete Task
**Feature**: Remove task by ID

#### Acceptance Criteria:
- System accepts task ID for deletion
- Task permanently removed from storage
- Confirmation message displayed
- Error message when task ID doesn't exist

### 2.5 US-005: Mark Complete/Incomplete
**Feature**: Toggle task completion status

#### Acceptance Criteria:
- Separate commands for marking complete and incomplete
- Updates task's completion status
- Updates the `updated_at` timestamp
- Confirmation message displayed
- Error message when task ID doesn't exist

---

## 3. Technical Architecture

### 3.1 Layered Architecture Implementation

#### Presentation Layer:
- Command-line interface using `argparse` or similar
- Console input/output handling
- User interaction flow management

#### Application Layer:
- Service functions coordinating operations
- Business logic orchestration
- Input validation and error handling

#### Domain Layer:
- Task entity definition with validation rules
- Business rule enforcement
- Core data structures and methods

#### Infrastructure Layer:
- Local file storage (JSON)
- Persistence mechanisms
- Data access operations

### 3.2 Technology Stack
- **Runtime**: Python 3.13+
- **Package Manager**: UV
- **Type Checking**: mypy (strict)
- **Linting/Format**: ruff
- **Storage**: Local JSON file

---

## 4. Data Model

### 4.1 Task Entity
```python
class Task:
    id: str (UUID)
    title: str (1-200 characters)
    description: str (optional, max 1000 characters)
    completed: bool (default False)
    created_at: datetime (auto-generated)
    updated_at: datetime (auto-generated)
```

### 4.2 Validation Rules
- Title: Required, 1-200 characters
- Description: Optional, max 1000 characters
- Completed: Boolean, defaults to False
- Timestamps: Auto-generated, never user-provided

---

## 5. User Interface

### 5.1 Command Structure
```
todo-cli [command] [arguments]

Commands:
- add --title "Title" [--description "Description"]
- list
- update --id ID [--title "New Title"] [--description "New Description"]
- delete --id ID
- complete --id ID
- uncomplete --id ID
```

### 5.2 Expected Output Formats
- **Add Task**: "Task 'X' created successfully with ID: Y"
- **List Tasks**: Formatted table with ID, Title, Status, Created Date
- **Update Task**: "Task 'X' updated successfully"
- **Delete Task**: "Task 'X' deleted successfully"
- **Complete Task**: "Task 'X' marked as complete"
- **Uncomplete Task**: "Task 'X' marked as incomplete"

---

## 6. Error Handling

### 6.1 Error Categories
- **Validation Errors**: Invalid input data
- **Not Found Errors**: Task ID doesn't exist
- **System Errors**: File I/O or storage issues

### 6.2 Error Messages
- User-friendly messages for all error conditions
- Specific error codes for debugging
- No stack traces in production mode

---

## 7. Security Considerations

### 7.1 Data Protection
- No sensitive data stored
- Local storage only
- Input sanitization at all boundaries

---

## 8. Quality Requirements

### 8.1 Testing Requirements
- Domain/Models: 100% coverage
- Services: 90% coverage
- CLI Commands: 85% coverage
- Test naming: `test_<action>_<condition>_<result>`

### 8.2 Documentation Requirements
- README.md with setup instructions
- Docstrings on all public interfaces
- CLI help text for all commands

---

## 9. Constraints

### 9.1 Performance
- Sub-second response times for all operations
- Efficient JSON parsing and writing

### 9.2 Size Limitations
- Maximum 200 lines per file
- Maximum 50 lines per function

---

## 10. Future Considerations

### 10.1 Phase Transition Preparation
- Domain layer designed for portability to Phase II
- Abstraction layers to support future infrastructure changes
- API contracts designed to support web interface in Phase II

---

**Version**: 1.0.0
**Created**: 2026-01-13
**Approved**: Pending

#### specs\todo-console-app\plan.md
# Architecture Plan: Phase I Console Todo App

## 1. Scope and Dependencies

### 1.1 In Scope
- Console application with add/view/update/delete/complete functionality
- Local file-based storage using JSON
- Command-line interface with rich formatting
- Task validation and business logic
- Unit and integration tests

### 1.2 Out of Scope
- Web interface (Phase II responsibility)
- User authentication (Phase II responsibility)
- Database integration (Phase II responsibility)
- Cloud synchronization
- Advanced reporting features

### 1.3 External Dependencies
- Python 3.13+ runtime
- Click library for CLI parsing
- Rich library for formatting
- Pydantic for data validation
- UUID for ID generation
- JSON for storage serialization

---

## 2. Key Decisions and Rationale

### 2.1 Storage Abstraction Layer
**Decision**: Implement abstract storage interface with JSON file implementation
- **Options Considered**: Direct file manipulation, abstract interface, ORM
- **Trade-offs**: Abstraction adds complexity but enables easy migration to Phase II
- **Rationale**: Enables seamless transition to database in Phase II as per constitution

### 2.2 CLI Framework Selection
**Decision**: Use Click library for command-line parsing
- **Options Considered**: argparse (built-in), Click, Typer
- **Trade-offs**: Click adds dependency but provides better UX and validation
- **Rationale**: Click offers superior argument validation and help generation

### 2.3 Formatting Library
**Decision**: Use Rich library for console output formatting
- **Options Considered**: Built-in print statements, Rich, Textual
- **Trade-offs**: Rich adds dependency but provides excellent formatting capabilities
- **Rationale**: Rich enables professional-looking table output and color support

### 2.4 Data Validation
**Decision**: Use Pydantic for data validation
- **Options Considered**: Manual validation, Pydantic, attrs
- **Trade-offs**: Pydantic adds dependency but provides robust validation
- **Rationale**: Aligns with constitution's emphasis on validation at domain layer

### 2.5 Dependency Injection
**Decision**: Implement DI for testability
- **Options Considered**: Global dependencies, DI container, constructor injection
- **Rationale**: Enables easier unit testing and follows SOLID principles

### 2.6 Principles
- **Measurable**: Max 200 lines per file, max 50 lines per function
- **Reversible**: Abstraction layers allow backend changes
- **Smallest Viable Change**: Minimal dependencies to achieve goals

---

## 3. Interfaces and API Contracts

### 3.1 Public APIs

#### CLI Interface:
```
todo-cli add --title "Title" [--description "Description"]
todo-cli list
todo-cli update --id ID [--title "New Title"] [--description "New Description"]
todo-cli delete --id ID
todo-cli complete --id ID
todo-cli uncomplete --id ID
```

#### Domain API:
```python
class Task(BaseModel):
    id: str
    title: str
    description: str
    completed: bool
    created_at: datetime
    updated_at: datetime

def create_task(title: str, description: str = "") -> Task
def get_all_tasks() -> List[Task]
def get_task_by_id(task_id: str) -> Task
def update_task(task_id: str, title: str = None, description: str = None) -> Task
def delete_task(task_id: str) -> bool
def mark_complete(task_id: str) -> Task
def mark_incomplete(task_id: str) -> Task
```

#### Storage API:
```python
class StorageInterface(ABC):
    def save_task(self, task: Task) -> Task
    def get_all_tasks(self) -> List[Task]
    def get_task_by_id(self, task_id: str) -> Task
    def update_task(self, task_id: str, **kwargs) -> Task
    def delete_task(self, task_id: str) -> bool
```

### 3.2 Versioning Strategy
- Semantic versioning (MAJOR.MINOR.PATCH)
- Backward compatible changes increment PATCH
- Breaking changes increment MINOR or MAJOR

### 3.3 Error Taxonomy
- `TaskNotFoundError`: Task ID not found (404 equivalent)
- `ValidationError`: Invalid input data (400 equivalent)
- `StorageError`: Storage operation failed (500 equivalent)

---

## 4. Non-Functional Requirements (NFRs) and Budgets

### 4.1 Performance
- **p95 Latency**: < 500ms for all operations
- **Throughput**: Handle up to 1000 tasks efficiently
- **Resource Caps**: < 50MB memory usage for typical operation

### 4.2 Reliability
- **SLOs**: 99.9% uptime for basic operations
- **Error Budget**: < 0.1% operation failures
- **Degradation Strategy**: Graceful degradation with error messages

### 4.3 Security
- **AuthN/AuthZ**: N/A for Phase I (local storage only)
- **Data Handling**: No sensitive data stored locally
- **Secrets**: No secrets in codebase
- **Auditing**: Basic operation logging

### 4.4 Cost
- **Unit Economics**: Free to run (local only)

---

## 5. Data Management and Migration

### 5.1 Source of Truth
- Local JSON file (`tasks.json`) for Phase I
- Will migrate to database in Phase II

### 5.2 Schema Evolution
- Version field in JSON schema for future evolution
- Backward compatibility maintained for Phase II

### 5.3 Migration and Rollback
- Simple JSON format allows manual migration
- Automated migration path planned for Phase II

### 5.4 Data Retention
- Local data retention based on user control
- No automatic cleanup policies

---

## 6. Operational Readiness

### 6.1 Observability
- **Logs**: Operation-level logging for debugging
- **Metrics**: Performance timing for operations
- **Traces**: Not required for Phase I

### 6.2 Alerting
- **Thresholds**: Not applicable for local console app
- **On-call Owners**: Not applicable

### 6.3 Runbooks
- **Common Tasks**: Setup, backup, restore procedures
- **Troubleshooting**: Common error resolution steps

### 6.4 Deployment and Rollback Strategies
- **Deployment**: Single binary distribution
- **Rollback**: Versioned releases with pip uninstall/install

### 6.5 Feature Flags
- Not applicable for Phase I

---

## 7. Risk Analysis and Mitigation

### 7.1 Top 3 Risks

1. **Large Data Set Performance**
   - **Risk**: Slow operations with many tasks
   - **Blast Radius**: Degraded UX
   - **Mitigation**: Lazy loading, indexing considerations for Phase II

2. **File Corruption**
   - **Risk**: JSON file corruption causing data loss
   - **Blast Radius**: Complete data loss
   - **Mitigation**: Backup copies, atomic writes

3. **Dependency Updates**
   - **Risk**: Breaking changes in external libraries
   - **Blast Radius**: Application instability
   - **Mitigation**: Pin versions, regular updates

### 7.2 Kill Switches/Guardrails
- Safe mode for corrupted data recovery
- Version compatibility checks

---

## 8. Evaluation and Validation

### 8.1 Definition of Done
- [ ] All 5 Basic Level features implemented
- [ ] 100% type coverage achieved
- [ ] Domain/Models: 100% test coverage
- [ ] Services: 90% test coverage
- [ ] CLI: 85% test coverage
- [ ] Architecture follows layered pattern

### 8.2 Output Validation
- Format: Properly formatted tables and messages
- Requirements: All user stories satisfied
- Safety: Proper input validation and error handling

---

## 9. Implementation Approach

### 9.1 Layer Implementation Order
1. **Domain Layer**: Task model and validation (first)
2. **Storage Layer**: Abstract interface and JSON implementation
3. **Service Layer**: Business logic functions
4. **CLI Layer**: Command-line interface

### 9.2 File Structure
```
src/
└── hackathon_todo/
    ├── __init__.py
    ├── __main__.py
    ├── cli/
    │   ├── __init__.py
    │   └── commands.py
    ├── domain/
    │   ├── __init__.py
    │   └── models.py
    ├── services/
    │   ├── __init__.py
    │   └── task_service.py
    └── storage/
        ├── __init__.py
        └── json_storage.py
```

### 9.3 Critical Files
- `domain/models.py`: Task model and validation
- `storage/json_storage.py`: Storage abstraction implementation
- `services/task_service.py`: Business logic coordination
- `cli/commands.py`: CLI command definitions

---

**Version**: 1.0.0
**Created**: 2026-01-13
**Approved**: Pending

#### specs\todo-console-app\tasks.md
# Task Breakdown: Phase I Console Todo App

## 1. Overview

This document outlines all atomic tasks required to implement the Phase I Console Todo App according to the specification and architecture plan. Each task is designed to be testable and implementable in isolation while maintaining the layered architecture.

---

## 2. Layer 1: Domain (Foundation)

### T-001: Create project structure with pyproject.toml and UV setup
**Description**: Set up the initial project structure and configuration files
- Create proper directory structure: `src/hackathon_todo/` with submodules
- Configure `pyproject.toml` with dependencies (click, rich, pydantic, etc.)
- Set up UV configuration and initial dependencies
- Ensure project follows Python packaging best practices

**Acceptance Criteria**:
- Project structure matches plan specification
- Dependencies properly configured in pyproject.toml
- Project can be installed in development mode with UV

**Dependencies**: None

### T-002: Create custom exception classes
**Description**: Implement custom exception hierarchy for proper error handling
- Create base `TodoAppError` exception class
- Create `ValidationError` for validation failures
- Create `NotFoundError` for missing resources
- Create `StorageError` for storage-related failures

**Acceptance Criteria**:
- All exception classes inherit from proper base classes
- Exceptions have appropriate docstrings
- Follow project's exception hierarchy pattern

**Dependencies**: None

### T-003: Create Task dataclass with validation logic
**Description**: Implement the core Task model with validation rules
- Create Task dataclass with id, title, description, completed, timestamps
- Implement validation for title (1-200 chars)
- Implement validation for description (max 1000 chars)
- Auto-generate ID and timestamps
- Include proper type hints and docstrings

**Acceptance Criteria**:
- Task model validates title length (1-200 chars)
- Task model validates description length (max 1000 chars)
- ID auto-generation works properly
- Timestamps auto-update appropriately
- All fields properly typed

**Dependencies**: T-002 (custom exceptions)

---

## 3. Layer 2: Storage

### T-004: Create abstract TaskStorage interface (ABC)
**Description**: Define the abstract storage interface for dependency inversion
- Create abstract base class `TaskStorage`
- Define abstract methods: save_task, get_all_tasks, get_task_by_id, update_task, delete_task
- Include proper type hints for all methods
- Add comprehensive docstrings

**Acceptance Criteria**:
- Abstract interface properly defined with ABC
- All required methods defined with proper signatures
- Type hints included for all methods
- Docstrings explain each method's purpose

**Dependencies**: T-003 (Task model)

### T-005: Implement InMemoryStorage class
**Description**: Create in-memory storage implementation for testing and development
- Implement `TaskStorage` interface
- Use dictionary for task storage
- Implement all required methods with proper validation
- Thread-safe operations if needed

**Acceptance Criteria**:
- All interface methods implemented
- Proper error handling for missing tasks
- Data persistence within application lifetime
- Follows interface contract exactly

**Dependencies**: T-004 (TaskStorage interface)

---

## 4. Layer 3: Services

### T-006: Create TaskService with CRUD operations
**Description**: Implement business logic service layer
- Create `TaskService` class
- Implement add_task method with validation
- Implement get_all_tasks method
- Implement get_task_by_id method
- Implement update_task method with validation
- Implement delete_task method
- Implement mark_complete method
- Implement mark_incomplete method
- Include proper error handling and validation

**Acceptance Criteria**:
- All CRUD operations implemented
- Proper validation performed on inputs
- Proper error handling with custom exceptions
- Updated_at timestamp updated on modifications
- Follows service layer patterns from architecture

**Dependencies**: T-003 (Task model), T-004 (TaskStorage interface), T-005 (InMemoryStorage)

---

## 5. Layer 4: CLI

### T-007: Create display module for formatted output
**Description**: Implement module for formatted console output
- Create module for table display of tasks
- Implement status formatting (⬜ Pending, ✅ Done)
- Create consistent formatting for all outputs
- Use Rich library for enhanced formatting

**Acceptance Criteria**:
- Tasks displayed in formatted table
- Status properly formatted with emojis
- Consistent formatting across all outputs
- Uses Rich library effectively

**Dependencies**: T-003 (Task model)

### T-008: Create command handlers
**Description**: Implement individual command handlers for all operations
- Create add_command handler
- Create list_command handler
- Create update_command handler
- Create delete_command handler
- Create complete_command handler
- Create uncomplete_command handler
- Each handler should validate inputs and call service layer

**Acceptance Criteria**:
- All command handlers implemented
- Proper input validation
- Error handling with user-friendly messages
- Calls service layer appropriately

**Dependencies**: T-006 (TaskService), T-007 (display module)

### T-009: Create main CLI app with command parsing
**Description**: Implement main CLI application with Click framework
- Set up Click application
- Register all command handlers
- Implement proper argument parsing
- Add help text and usage information
- Handle command errors gracefully

**Acceptance Criteria**:
- CLI application properly configured
- All commands registered and accessible
- Proper argument parsing and validation
- Helpful error messages
- Follows Click framework best practices

**Dependencies**: T-008 (command handlers)

### T-010: Create __main__.py entry point
**Description**: Create application entry point
- Create main entry point that runs CLI application
- Proper error handling at application level
- Exit codes for different error conditions

**Acceptance Criteria**:
- Entry point properly configured
- CLI application runs when module executed
- Proper error handling and exit codes

**Dependencies**: T-009 (main CLI app)

---

## 6. Layer 5: Quality

### T-011: Create tests for domain models
**Description**: Implement comprehensive tests for domain layer
- Test Task model validation
- Test custom exception classes
- Test edge cases for validation
- Achieve 100% test coverage for domain

**Acceptance Criteria**:
- 100% test coverage for domain layer
- All validation rules tested
- Edge cases covered
- Tests follow naming convention: `test_<action>_<condition>_<result>`

**Dependencies**: T-002 (custom exceptions), T-003 (Task model)

### T-012: Create tests for services
**Description**: Implement comprehensive tests for service layer
- Test all service methods
- Test error conditions
- Test validation in service layer
- Achieve 90% test coverage for services

**Acceptance Criteria**:
- 90% test coverage for service layer
- All business logic tested
- Error conditions properly handled
- Tests follow naming convention

**Dependencies**: T-006 (TaskService)

### T-013: Create tests for CLI commands
**Description**: Implement tests for CLI interface
- Test all CLI commands
- Test argument validation
- Test error handling in CLI
- Achieve 85% test coverage for CLI

**Acceptance Criteria**:
- 85% test coverage for CLI layer
- All commands tested with various inputs
- Error conditions tested
- Tests follow naming convention

**Dependencies**: T-009 (main CLI app)

### T-014: Create README.md with setup instructions
**Description**: Create comprehensive README with setup and usage instructions
- Installation instructions
- Usage examples for all commands
- Project structure explanation
- Contribution guidelines

**Acceptance Criteria**:
- Clear installation instructions
- Examples for all commands
- Project structure explained
- Meets quality requirements from constitution

**Dependencies**: All other tasks (as it documents the complete application)

---

## 7. Task Dependencies Summary

```
T-001: Create project structure
T-002: Create custom exceptions
T-003: Create Task model (depends on T-002)
T-004: Create TaskStorage interface (depends on T-003)
T-005: Implement InMemoryStorage (depends on T-004)
T-006: Create TaskService (depends on T-003, T-004, T-005)
T-007: Create display module (depends on T-003)
T-008: Create command handlers (depends on T-006, T-007)
T-009: Create main CLI app (depends on T-008)
T-010: Create entry point (depends on T-009)
T-011: Domain tests (depends on T-002, T-003)
T-012: Service tests (depends on T-006)
T-013: CLI tests (depends on T-009)
T-014: README (depends on all tasks)
```

---

## 8. Implementation Order

1. Foundation: T-001, T-002, T-003
2. Storage: T-004, T-005
3. Services: T-006
4. CLI: T-007, T-008, T-009, T-010
5. Quality: T-011, T-012, T-013, T-014

---

**Version**: 1.0.0
**Created**: 2026-01-13
**Approved**: Pending

#### specs\phase-ii-full-stack-web-app\spec.md
# Phase II: Full-Stack Web Application Specification

## 1. Feature Overview

### 1.1 Description
Transform the existing console application into a multi-user web application with persistent storage. The application will provide a complete task management system with user authentication, allowing individual users to manage their personal tasks in a secure manner.

### 1.2 Goals
- Enable multi-user access to the task management system
- Implement persistent storage using PostgreSQL database
- Provide secure authentication and authorization
- Create a responsive web interface using modern web technologies

### 1.3 Success Criteria
- Users can register, login, and logout securely
- Users can perform all task operations (CRUD) on their own tasks only
- System properly enforces user isolation
- Application meets all technical requirements specified

## 2. User Stories

### US-101: User Registration
**As a** visitor,
**I want** to create an account with email and password,
**So that** I can use the task management system.

**Acceptance Criteria:**
- Email must be validated for proper format (contains @ and domain)
- Password must be minimum 8 characters
- System rejects duplicate email addresses
- User receives confirmation upon successful registration
- Error message displayed for invalid inputs

### US-102: User Login
**As a** user,
**I want** to sign in with my credentials,
**So that** I can access my personal task list.

**Acceptance Criteria:**
- System returns JWT token upon successful authentication
- Invalid credentials result in appropriate error message
- User session is established after login
- Login attempts are rate-limited to prevent brute force

### US-103: User Logout
**As a** user,
**I want** to sign out,
**So that** my session is terminated securely.

**Acceptance Criteria:**
- Session/token is invalidated on logout
- User is redirected to login screen
- User cannot access protected routes after logout

### US-104: Add Task (Authenticated)
**As a** logged-in user,
**I want** to create a task,
**So that** I can track my responsibilities.

**Acceptance Criteria:**
- Task is associated with authenticated user ID
- Task title must be 1-200 characters
- Task description must be maximum 1000 characters
- Task is persisted in the database
- Validation errors are displayed appropriately

### US-105: View My Tasks
**As a** logged-in user,
**I want** to see only my tasks,
**So that** I can manage my personal responsibilities.

**Acceptance Criteria:**
- Only tasks belonging to the authenticated user are displayed
- Other users' tasks are not accessible
- Tasks can be filtered by status (all/pending/completed)
- Pagination implemented for large task lists

### US-106: Update My Task
**As a** logged-in user,
**I want** to update my own tasks,
**So that** I can keep my task information current.

**Acceptance Criteria:**
- User can only update tasks they own
- Attempt to update another user's task results in error
- Updated task is saved to the database
- Validation rules apply to updates

### US-107: Delete My Task
**As a** logged-in user,
**I want** to delete my own tasks,
**So that** I can remove completed or irrelevant tasks.

**Acceptance Criteria:**
- User can only delete tasks they own
- Attempt to delete another user's task results in error
- Task is removed from the database
- Confirmation prompt before deletion

### US-108: Complete My Task
**As a** logged-in user,
**I want** to toggle completion on my tasks,
**So that** I can mark tasks as done.

**Acceptance Criteria:**
- User can only modify completion status of their own tasks
- Attempt to modify another user's task results in error
- Task completion status is updated in the database
- Visual indication of completion status in UI

## 3. Technical Requirements

### 3.1 Architecture
- Frontend: Next.js 16+ (App Router), TypeScript, Tailwind CSS
- Backend: FastAPI, SQLModel, Neon PostgreSQL
- Authentication: Better Auth with JWT
- Database: Neon PostgreSQL (managed PostgreSQL service)

### 3.2 Frontend Requirements
- Responsive design supporting desktop and mobile
- Type-safe TypeScript implementation
- Modern UI with Tailwind CSS
- Client-side routing with Next.js App Router
- Form validation and error handling
- Loading states and user feedback

### 3.3 Backend Requirements
- RESTful API design with proper HTTP status codes
- JWT-based authentication middleware
- Database models with proper relationships
- Input validation and sanitization
- Proper error handling and logging
- Rate limiting for authentication endpoints

### 3.4 Security Requirements
- All endpoints require authentication except signup/signin
- User data isolation enforced at API layer
- Passwords stored securely (hashed)
- JWT tokens properly configured with expiration
- Protection against common vulnerabilities (XSS, CSRF, etc.)

### 3.5 Database Schema
#### Users Table
- id (UUID, Primary Key)
- email (VARCHAR, Unique, Not Null)
- password_hash (VARCHAR, Not Null)
- created_at (TIMESTAMP, Not Null)
- updated_at (TIMESTAMP, Not Null)

#### Tasks Table
- id (UUID, Primary Key)
- user_id (UUID, Foreign Key to Users, Not Null)
- title (VARCHAR 1-200 chars, Not Null)
- description (VARCHAR max 1000 chars)
- completed (BOOLEAN, Default False)
- created_at (TIMESTAMP, Not Null)
- updated_at (TIMESTAMP, Not Null)

## 4. API Specification

### 4.1 Authentication Endpoints
- POST /api/auth/register - User registration
- POST /api/auth/login - User login
- POST /api/auth/logout - User logout

### 4.2 Task Endpoints
- GET /api/tasks - Get user's tasks (with optional status filter)
- POST /api/tasks - Create a new task
- PUT /api/tasks/{id} - Update a task
- DELETE /api/tasks/{id} - Delete a task
- PATCH /api/tasks/{id}/complete - Toggle task completion

### 4.3 Authentication Middleware
- All task endpoints require valid JWT token
- Token verification and user identification
- Access control to ensure users can only access their own tasks

## 5. Implementation Constraints

### 5.1 Performance
- API responses should be < 500ms for typical operations
- Database queries should be optimized with proper indexing
- Frontend should implement proper loading states

### 5.2 Scalability
- Database schema designed to handle multiple users efficiently
- Authentication system should scale with user growth
- Caching strategies for improved performance

### 5.3 Maintainability
- Clean separation of concerns between frontend and backend
- Proper error handling and logging
- Comprehensive input validation
- Well-documented code with TypeScript types

## 6. Dependencies
- Next.js 16+
- FastAPI
- SQLModel
- Neon PostgreSQL
- Better Auth
- TypeScript
- Tailwind CSS
- PostgreSQL driver for Python

## 7. Acceptance Tests

### 7.1 Authentication Tests
- Verify registration with valid credentials creates user
- Verify registration with invalid email fails
- Verify registration with weak password fails
- Verify login with correct credentials returns JWT
- Verify login with incorrect credentials fails
- Verify logout invalidates session

### 7.2 Task Management Tests
- Verify user can create task after authentication
- Verify user can retrieve only their own tasks
- Verify user cannot access another user's tasks
- Verify user can update only their own tasks
- Verify user can delete only their own tasks
- Verify user can toggle completion of only their own tasks
- Verify task validation rules are enforced

### 7.3 Security Tests
- Verify unauthenticated access to task endpoints fails
- Verify authenticated user cannot access other users' tasks
- Verify JWT tokens expire appropriately
- Verify password hashing works correctly

#### specs\phase-ii-full-stack-web-app\plan.md
# Phase II: Full-Stack Web Application - Architecture Plan

## 1. Executive Summary

This document outlines the architectural plan for transforming the existing console application into a full-stack web application with multi-user support and persistent storage. The solution will leverage Next.js for the frontend, FastAPI for the backend, and Neon PostgreSQL for the database, with Better Auth for authentication.

## 2. Architecture Overview

### 2.1 High-Level Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Browser       │    │   Load Balancer  │    │   Neon         │
│                 │    │                  │    │   PostgreSQL   │
│  Next.js App    │◄──►│   FastAPI        │◄──►│   Database     │
│  (Frontend)     │    │   (Backend)      │    │                │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              ▲
                              │
                       ┌──────────────┐
                       │ Better Auth  │
                       │ (JWT)        │
                       └──────────────┘
```

### 2.2 System Boundaries
- **Frontend**: Next.js application handling user interface and authentication
- **Backend**: FastAPI service managing business logic and data persistence
- **Database**: Neon PostgreSQL storing user and task data
- **Authentication Service**: Better Auth handling user registration/login

## 3. Monorepo Structure

```
hackathon-todo/
├── frontend/                    # Next.js 16+ App
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx        # Landing/redirect
│   │   │   ├── (auth)/
│   │   │   │   ├── login/page.tsx
│   │   │   │   └── signup/page.tsx
│   │   │   └── dashboard/
│   │   │       └── page.tsx    # Task management
│   │   ├── components/
│   │   │   ├── ui/             # Button, Input, Card
│   │   │   ├── auth/           # LoginForm, SignupForm
│   │   │   └── tasks/          # TaskList, TaskCard, TaskForm
│   │   ├── lib/
│   │   │   ├── api.ts          # Backend API client
│   │   │   ├── auth.ts         # Better Auth client
│   │   │   └── utils.ts
│   │   └── types/
│   │       └── index.ts
│   ├── package.json
│   ├── tailwind.config.ts
│   └── tsconfig.json
├── backend/
│   ├── src/
│   │   └── hackathon_todo_api/
│   │       ├── __init__.py
│   │       ├── main.py         # FastAPI app
│   │       ├── config.py       # Settings
│   │       ├── database.py     # Neon connection
│   │       ├── models/
│   │       │   ├── __init__.py
│   │       │   ├── user.py     # User model (Better Auth managed)
│   │       │   └── task.py     # Task SQLModel
│   │       ├── schemas/
│   │       │   ├── __init__.py
│   │       │   └── task.py     # Pydantic schemas
│   │       ├── routes/
│   │       │   ├── __init__.py
│   │       │   ├── health.py   # Health check
│   │       │   └── tasks.py    # Task CRUD endpoints
│   │       ├── services/
│   │       │   ├── __init__.py
│   │       │   └── task_service.py
│   │       └── auth/
│   │           ├── __init__.py
│   │           └── jwt.py      # JWT verification
│   ├── pyproject.toml
│   └── alembic/                # DB migrations
├── docker-compose.yml
├── specs/
├── CLAUDE.md
└── README.md
```

## 4. Key Design Decisions

### 4.1 Monorepo Approach
- **Rationale**: Simplifies development, versioning, and deployment coordination
- **Benefits**: Shared types, easier cross-team collaboration, atomic commits
- **Trade-offs**: Larger repository size, potential for tight coupling if not managed properly

### 4.2 Authentication Strategy
- **Frontend**: Better Auth handles signup/login and issues JWT
- **Backend**: JWT verification middleware extracts user identity
- **Rationale**: Better Auth provides robust authentication with minimal setup
- **Security**: All endpoints require authentication except public routes

### 4.3 Data Isolation Strategy
- **Mechanism**: All database queries filtered by authenticated user_id
- **Implementation**: Middleware adds user_id to request context
- **Enforcement**: Database-level and application-level checks

### 4.4 Technology Stack Selection

| Component | Technology | Rationale |
|-----------|------------|-----------|
| Frontend | Next.js 16+ | SSR, App Router, TypeScript integration |
| Styling | Tailwind CSS | Utility-first, rapid development |
| Backend | FastAPI | Async performance, automatic docs, Pydantic integration |
| ORM | SQLModel | Typed SQL models with Pydantic compatibility |
| Database | Neon PostgreSQL | Cloud-native, serverless, compatible with PostgreSQL |
| Auth | Better Auth | Modern, JWT-based, easy integration |

## 5. Detailed Architecture Components

### 5.1 Frontend Architecture

#### 5.1.1 Application Structure
- **Pages**: Next.js App Router for navigation
- **Components**: Modular, reusable UI components
- **State Management**: React state/hooks for local state, Better Auth for auth state
- **API Client**: Custom wrapper around fetch for backend communication

#### 5.1.2 Authentication Flow
1. User navigates to `/signup` or `/login`
2. Better Auth handles credentials
3. JWT token stored in browser (httpOnly cookie or localStorage)
4. Token attached to all subsequent API requests
5. Token refresh mechanism implemented

#### 5.1.3 Task Management UI
- **Dashboard Page**: Shows user's tasks with filtering
- **Task Form**: For creating/updating tasks
- **Task Cards**: Display individual tasks with action buttons
- **Loading States**: Proper UX during API calls

### 5.2 Backend Architecture

#### 5.2.1 API Layer
- **FastAPI Application**: Main entry point with CORS configuration
- **Route Modules**: Organized by feature (health, tasks)
- **Dependency Injection**: For database sessions and auth validation

#### 5.2.2 Business Logic Layer
- **Services**: TaskService for encapsulating business logic
- **Validation**: Input validation using Pydantic schemas
- **Error Handling**: Custom exceptions with proper HTTP status codes

#### 5.2.3 Data Layer
- **SQLModels**: Typed database models
- **Database Session**: Async SQLAlchemy session management
- **Migrations**: Alembic for schema evolution

#### 5.2.4 Authentication Layer
- **JWT Verification**: Middleware to validate tokens
- **User Context**: Extract user_id from token for authorization
- **Authorization**: Ensure users can only access their own data

## 6. Authentication Flow

```
1. User registers/login via Better Auth client
   ↓
2. Better Auth creates JWT token
   ↓
3. Frontend stores token securely
   ↓
4. Frontend sends token in Authorization header
   ↓
5. Backend verifies JWT signature and expiration
   ↓
6. Backend extracts user_id from token payload
   ↓
7. All database queries filtered by user_id
   ↓
8. Response returned to authenticated user
```

## 7. API Design

### 7.1 Base URL Convention
- Base: `/api/v1`
- Authentication: All endpoints require `Authorization: Bearer <token>`
- User isolation: Routes include user context (either implicit from token or explicit in path)

### 7.2 Authentication Endpoints
```
POST /api/v1/auth/register    - Create new user
POST /api/v1/auth/login       - Authenticate user
POST /api/v1/auth/logout      - Invalidate session
```

### 7.3 Task Management Endpoints
```
GET    /api/v1/tasks           - Get user's tasks (with optional status filter)
POST   /api/v1/tasks           - Create new task for authenticated user
PUT    /api/v1/tasks/{id}      - Update user's task
DELETE /api/v1/tasks/{id}      - Delete user's task
PATCH  /api/v1/tasks/{id}/complete - Toggle task completion
```

### 7.3 API Response Format
```json
{
  "success": true,
  "data": {},
  "message": "Operation completed successfully"
}
```

## 8. Database Schema

### 8.1 Users Table (Managed by Better Auth)
```sql
-- Better Auth manages users table
-- We'll extend with custom fields if needed
```

### 8.2 Tasks Table
```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,  -- From Better Auth
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index for user isolation
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
-- Index for filtering by completion status
CREATE INDEX idx_tasks_completed ON tasks(completed);
```

## 9. Security Considerations

### 9.1 Authentication & Authorization
- JWT tokens with appropriate expiration times
- Secure token storage (consider httpOnly cookies)
- Proper validation of user identity on each request
- Role-based access control if needed in future

### 9.2 Input Validation
- Server-side validation for all inputs
- SQL injection prevention through parameterized queries
- XSS prevention through proper output encoding

### 9.3 Data Protection
- User data isolation enforced at database level
- PII protection and privacy compliance
- Secure transmission with HTTPS

## 10. Performance Considerations

### 10.1 Caching Strategy
- API response caching for static content
- Database query result caching
- CDN for static assets

### 10.2 Database Optimization
- Proper indexing for common query patterns
- Connection pooling for database connections
- Query optimization and pagination for large datasets

### 10.3 Frontend Performance
- Code splitting and lazy loading
- Image optimization
- Bundle size optimization

## 11. Deployment Architecture

### 11.1 Containerization
- Docker containers for both frontend and backend
- Docker Compose for local development
- Environment-specific configurations

### 11.2 Infrastructure
- Frontend: Vercel, Netlify, or similar hosting
- Backend: Container orchestration (Docker Swarm, Kubernetes)
- Database: Neon PostgreSQL cloud service
- CDN: For static asset delivery

## 12. Monitoring and Observability

### 12.1 Logging
- Structured logging with appropriate log levels
- Request tracing across services
- Error tracking and alerting

### 12.2 Metrics
- API response times
- Database query performance
- User activity metrics
- Resource utilization

## 13. Testing Strategy

### 13.1 Unit Testing
- Backend: FastAPI test client for API endpoints
- Frontend: Jest/React Testing Library for components
- Services: Isolated business logic testing

### 13.2 Integration Testing
- End-to-end authentication flows
- API database integration tests
- Frontend-backend integration tests

### 13.3 Security Testing
- Authentication bypass attempts
- Authorization checks
- Input validation testing

## 14. Risk Analysis

### 14.1 Technical Risks
- **Authentication Complexity**: Better Auth integration might have limitations
  - *Mitigation*: Thorough testing, fallback strategies
- **Database Scaling**: Neon PostgreSQL performance under load
  - *Mitigation*: Performance testing, monitoring, scaling plan
- **Frontend Bundle Size**: Large bundle affecting load times
  - *Mitigation*: Code splitting, optimization tools

### 14.2 Security Risks
- **Token Theft**: JWT tokens could be stolen
  - *Mitigation*: Short expiration, refresh tokens, secure storage
- **Data Isolation**: Cross-user data access if validation fails
  - *Mitigation*: Multiple validation layers, audit trails

## 15. Implementation Phases

### Phase 1: Foundation
- Set up monorepo structure
- Configure authentication with Better Auth
- Create basic database schema
- Implement health check endpoints

### Phase 2: Core Features
- Implement task CRUD operations
- Create basic UI components
- Connect frontend to backend APIs
- Implement user isolation

### Phase 3: Enhancement
- Add filtering and sorting capabilities
- Implement advanced UI features
- Add comprehensive error handling
- Performance optimizations

## 16. Success Criteria

- [ ] Authentication system works reliably
- [ ] Users can only access their own data
- [ ] All API endpoints return correct responses
- [ ] Frontend UI is responsive and intuitive
- [ ] Performance meets requirements (<500ms response time)
- [ ] Security measures are properly implemented
- [ ] Application is deployable and scalable

#### specs\phase-ii-full-stack-web-app\tasks.md
# Phase II Full-Stack Web Application - Task Breakdown

## Overview
This document outlines all implementation tasks required to transform the console app into a multi-user web application with persistent storage. Tasks are organized in dependency order to ensure smooth development progression.

## Layer 1: Project Setup

### T-201: Create frontend folder with Next.js 16+ App Router setup
**Description**: Initialize Next.js project with App Router, TypeScript, and basic configuration
**Dependencies**: None
**Acceptance Criteria**:
- Next.js 16+ project created with App Router
- TypeScript configured
- Basic ESLint and Prettier setup
- Project builds and runs without errors
**Test Cases**:
- `npm run dev` starts development server
- `npm run build` creates production build

### T-202: Create backend folder with FastAPI + UV setup
**Description**: Initialize FastAPI project with proper Python packaging using UV
**Dependencies**: None
**Acceptance Criteria**:
- FastAPI project structure created
- pyproject.toml with proper dependencies
- UV package manager configured
- Basic Hello World endpoint works
**Test Cases**:
- `uv run uvicorn src.hackathon_todo_api.main:app --reload` starts server
- GET / returns "Hello World"

### T-203: Create docker-compose.yml for local development
**Description**: Set up Docker Compose for local development environment
**Dependencies**: T-201, T-202
**Acceptance Criteria**:
- docker-compose.yml defines frontend, backend, and database services
- Environment variables properly configured
- Services can communicate with each other
**Test Cases**:
- `docker-compose up` starts all services
- Frontend can connect to backend
- Backend can connect to database

### T-204: Setup Neon PostgreSQL database and get connection string
**Description**: Create Neon PostgreSQL database and configure connection
**Dependencies**: None
**Acceptance Criteria**:
- Neon PostgreSQL database created
- Connection string obtained
- Database accessible from local environment
**Test Cases**:
- Connection string allows connection to database
- Basic query executes successfully

## Layer 2: Backend - Database & Models

### T-205: Create database.py with async Neon connection
**Description**: Set up async database connection using Neon PostgreSQL
**Dependencies**: T-202, T-204
**Acceptance Criteria**:
- Database connection module created
- Async connection pool configured
- Connection string properly handled
**Test Cases**:
- Database connection can be established
- Connection closes properly after use

### T-206: Create Task SQLModel in models/task.py
**Description**: Define Task model using SQLModel with proper relationships
**Dependencies**: T-202, T-205
**Acceptance Criteria**:
- Task model with id, user_id, title, description, completed, timestamps
- Proper validation for title length (1-200) and description (max 1000)
- Model inherits from SQLModel with proper table configuration
**Test Cases**:
- Model can be instantiated with valid data
- Validation fails with invalid data

### T-207: Create Pydantic schemas in schemas/task.py
**Description**: Create Pydantic schemas for request/response validation
**Dependencies**: T-202, T-206
**Acceptance Criteria**:
- TaskCreate schema with required fields (title, description)
- TaskRead schema with all fields including ID
- TaskUpdate schema with optional fields
- Proper validation matching Phase I requirements
**Test Cases**:
- Schemas validate correct data
- Schemas reject invalid data with appropriate errors

### T-208: Setup Alembic migrations and run initial migration
**Description**: Configure Alembic for database schema migrations
**Dependencies**: T-205, T-206
**Acceptance Criteria**:
- Alembic configured with proper database URL
- Initial migration created for Task model
- Migration can be applied successfully
**Test Cases**:
- `alembic upgrade head` applies migration
- Table exists in database after migration

## Layer 3: Backend - Auth

### T-209: Create config.py with environment settings
**Description**: Set up configuration management for environment variables
**Dependencies**: T-202
**Acceptance Criteria**:
- Settings class with proper validation
- Environment variables for database, JWT secret, etc.
- Different configurations for development, staging, production
**Test Cases**:
- Settings load correctly from environment
- Missing required variables raise appropriate errors

### T-210: Create JWT verification middleware in auth/jwt.py
**Description**: Implement JWT token verification and user extraction
**Dependencies**: T-202, T-209
**Acceptance Criteria**:
- JWT verification function created
- User ID extracted from token
- Invalid tokens properly rejected
**Test Cases**:
- Valid token returns user ID
- Invalid/expired token raises appropriate exception

### T-211: Create user validation dependency (URL user_id matches token)
**Description**: Create FastAPI dependency to validate user access rights
**Dependencies**: T-210
**Acceptance Criteria**:
- Dependency function that compares URL user_id with token user_id
- Proper error response when user_id mismatch occurs
- Integration with FastAPI security system
**Test Cases**:
- Matching user_ids pass validation
- Mismatching user_ids return 403 Forbidden

## Layer 4: Backend - API Routes

### T-212: Create health check endpoint
**Description**: Implement basic health check endpoint for monitoring
**Dependencies**: T-202
**Acceptance Criteria**:
- GET /health endpoint returns status
- Endpoint indicates system readiness
**Test Cases**:
- GET /health returns 200 with status object

### T-213: Create TaskService with async CRUD operations
**Description**: Implement service layer with async database operations
**Dependencies**: T-205, T-206, T-207
**Acceptance Criteria**:
- getAllTasks method with user filtering
- createTask method with validation
- getTaskById method with user validation
- updateTask method with user validation
- deleteTask method with user validation
- toggleComplete method with user validation
**Test Cases**:
- All methods execute successfully with valid data
- Methods properly filter by user_id
- Validation occurs before database operations

### T-214: Create GET /api/{user_id}/tasks endpoint
**Description**: Implement endpoint to retrieve user's tasks with filtering
**Dependencies**: T-211, T-213
**Acceptance Criteria**:
- Endpoint accepts user_id from URL
- Authenticates user via JWT
- Filters tasks by user_id
- Optional status filtering (all/pending/completed)
- Returns properly formatted response
**Test Cases**:
- Authenticated user retrieves own tasks
- Unauthenticated request returns 401
- Unauthorized user access returns 403
- Status filtering works correctly

### T-215: Create POST /api/{user_id}/tasks endpoint
**Description**: Implement endpoint to create new task for user
**Dependencies**: T-211, T-213, T-207
**Acceptance Criteria**:
- Endpoint accepts user_id from URL
- Validates input using TaskCreate schema
- Creates task associated with user_id
- Returns created task with 201 status
**Test Cases**:
- Valid task creation returns 201 with created task
- Validation errors return 422
- Unauthorized access returns 403

### T-216: Create GET /api/{user_id}/tasks/{id} endpoint
**Description**: Implement endpoint to retrieve specific task
**Dependencies**: T-211, T-213
**Acceptance Criteria**:
- Endpoint accepts user_id and task_id from URL
- Validates user owns the task
- Returns task details if authorized
**Test Cases**:
- Authorized user retrieves own task
- Unauthorized user access returns 403
- Non-existent task returns 404

### T-217: Create PUT /api/{user_id}/tasks/{id} endpoint
**Description**: Implement endpoint to update user's task
**Dependencies**: T-211, T-213, T-207
**Acceptance Criteria**:
- Endpoint accepts user_id and task_id from URL
- Validates user owns the task
- Updates task with provided data
- Returns updated task
**Test Cases**:
- Authorized user updates own task
- Unauthorized user update returns 403
- Validation errors return 422

### T-218: Create DELETE /api/{user_id}/tasks/{id} endpoint
**Description**: Implement endpoint to delete user's task
**Dependencies**: T-211, T-213
**Acceptance Criteria**:
- Endpoint accepts user_id and task_id from URL
- Validates user owns the task
- Deletes task and returns success response
**Test Cases**:
- Authorized user deletes own task
- Unauthorized user delete returns 403
- Non-existent task returns 404

### T-219: Create PATCH /api/{user_id}/tasks/{id}/complete endpoint
**Description**: Implement endpoint to toggle task completion status
**Dependencies**: T-211, T-213
**Acceptance Criteria**:
- Endpoint accepts user_id and task_id from URL
- Validates user owns the task
- Toggles completed status
- Returns updated task
**Test Cases**:
- Authorized user toggles completion status
- Unauthorized user toggle returns 403
- Non-existent task returns 404

## Layer 5: Frontend - Setup & Auth

### T-220: Configure Tailwind CSS and base styles
**Description**: Set up Tailwind CSS with proper configuration
**Dependencies**: T-201
**Acceptance Criteria**:
- Tailwind CSS properly installed and configured
- Base styles applied to application
- Responsive design utilities available
**Test Cases**:
- Tailwind classes apply correctly to elements
- Responsive breakpoints work

### T-221: Setup Better Auth client in lib/auth.ts
**Description**: Configure Better Auth for frontend authentication
**Dependencies**: T-201
**Acceptance Criteria**:
- Better Auth client configured
- Authentication state management
- JWT token handling
**Test Cases**:
- User can authenticate successfully
- Token is stored and retrieved properly

### T-222: Create login page at (auth)/login/page.tsx
**Description**: Create login page with form and submission handling
**Dependencies**: T-221, T-220
**Acceptance Criteria**:
- Login form with email and password fields
- Form validation and error handling
- Redirect after successful login
**Test Cases**:
- Valid credentials allow login
- Invalid credentials show error message
- Successful login redirects to dashboard

### T-223: Create signup page at (auth)/signup/page.tsx
**Description**: Create signup page with registration form
**Dependencies**: T-221, T-220
**Acceptance Criteria**:
- Registration form with email and password fields
- Form validation and error handling
- Redirect after successful registration
**Test Cases**:
- Valid credentials allow registration
- Invalid credentials show error message
- Existing email shows appropriate error
- Successful registration redirects to dashboard

### T-224: Create auth middleware for protected routes
**Description**: Implement middleware to protect authenticated routes
**Dependencies**: T-221
**Acceptance Criteria**:
- Middleware checks authentication status
- Redirects unauthenticated users to login
- Allows authenticated users to access protected pages
**Test Cases**:
- Unauthenticated access redirects to login
- Authenticated access proceeds normally

## Layer 6: Frontend - API Client

### T-225: Create types in types/index.ts
**Description**: Define TypeScript interfaces for API entities
**Dependencies**: T-201
**Acceptance Criteria**:
- Task interface matching backend schema
- API response interface
- Form data interfaces
**Test Cases**:
- Types compile without errors
- Interfaces match backend schemas

### T-226: Create API client in lib/api.ts with JWT handling
**Description**: Implement API client with authentication headers
**Dependencies**: T-221, T-225
**Acceptance Criteria**:
- HTTP client with proper error handling
- Automatic JWT token attachment
- Consistent response format
**Test Cases**:
- API calls include authorization header when authenticated
- Errors are properly caught and formatted

## Layer 7: Frontend - UI Components

### T-227: Create Button, Input, Card components in components/ui/
**Description**: Create reusable UI components with Tailwind styling
**Dependencies**: T-220
**Acceptance Criteria**:
- Reusable Button component with variants
- Input component with validation support
- Card component for content grouping
**Test Cases**:
- Components render with proper styling
- Components accept props correctly

### T-228: Create LoginForm and SignupForm in components/auth/
**Description**: Create form components for authentication
**Dependencies**: T-227, T-221
**Acceptance Criteria**:
- Forms with proper validation
- Error display for failed submissions
- Loading states during submission
**Test Cases**:
- Forms validate input properly
- Submission errors are displayed
- Loading states work correctly

### T-229: Create TaskCard component in components/tasks/
**Description**: Create component to display individual task
**Dependencies**: T-227, T-225
**Acceptance Criteria**:
- Displays task title, description, and status
- Toggle completion button
- Delete button
- Proper styling for completed tasks
**Test Cases**:
- Task details display correctly
- Completion toggle works
- Delete button functions

### T-230: Create TaskList component in components/tasks/
**Description**: Create component to display list of tasks with filtering
**Dependencies**: T-229, T-225
**Acceptance Criteria**:
- Displays multiple TaskCards
- Filtering controls (all/pending/completed)
- Loading state when fetching tasks
**Test Cases**:
- Tasks display in list format
- Filtering works correctly
- Loading state shows during fetch

### T-231: Create TaskForm (add/edit) component in components/tasks/
**Description**: Create form for adding and editing tasks
**Dependencies**: T-227, T-225
**Acceptance Criteria**:
- Form for creating new tasks
- Form for editing existing tasks
- Validation matching backend requirements
**Test Cases**:
- Form validates title length (1-200 chars)
- Form validates description length (max 1000 chars)
- Submit creates/updates task correctly

## Layer 8: Frontend - Pages

### T-232: Create layout.tsx with auth provider
**Description**: Create root layout with authentication context
**Dependencies**: T-221
**Acceptance Criteria**:
- Layout wraps entire application
- Auth context provided to children
- Global styles applied
**Test Cases**:
- Authentication state available throughout app
- Layout renders consistently

### T-233: Create landing page (page.tsx) with redirect logic
**Description**: Create homepage that redirects based on auth status
**Dependencies**: T-232, T-221
**Acceptance Criteria**:
- Unauthenticated users see landing information
- Authenticated users redirected to dashboard
- Proper navigation links
**Test Cases**:
- Unauthenticated users see landing page
- Authenticated users redirect to dashboard

### T-234: Create dashboard page with task management
**Description**: Create main task management interface
**Dependencies**: T-230, T-231, T-226
**Acceptance Criteria**:
- Displays user's tasks using TaskList
- Form to add new tasks using TaskForm
- Filtering capability
- Responsive design
**Test Cases**:
- Tasks load and display correctly
- New tasks can be added
- Filtering works as expected
- UI is responsive on different devices

## Layer 9: Quality & Deployment

### T-235: Create backend tests for auth and task routes
**Description**: Write comprehensive tests for backend functionality
**Dependencies**: All backend tasks (T-205-T-219)
**Acceptance Criteria**:
- Unit tests for TaskService
- Integration tests for all API endpoints
- Authentication tests
- Error condition tests
**Test Cases**:
- All tests pass
- Coverage >80% for critical functionality

### T-236: Create frontend tests for components
**Description**: Write tests for frontend components and pages
**Dependencies**: All frontend tasks (T-220-T-234)
**Acceptance Criteria**:
- Unit tests for UI components
- Integration tests for page flows
- Authentication flow tests
**Test Cases**:
- All tests pass
- Critical user flows tested

### T-237: Update README.md with Phase II setup instructions
**Description**: Update documentation with new setup instructions
**Dependencies**: All tasks
**Acceptance Criteria**:
- Clear instructions for local development
- Environment variable requirements
- Deployment instructions
**Test Cases**:
- Instructions allow successful setup by new developer

### T-238: Deploy frontend to Vercel
**Description**: Deploy frontend application to production hosting
**Dependencies**: T-234, T-237
**Acceptance Criteria**:
- Frontend deployed to Vercel
- Connected to production backend
- SSL certificate configured
**Test Cases**:
- Application loads at deployed URL
- All functionality works as expected

### T-239: Deploy backend to Railway/Render
**Description**: Deploy backend API to production hosting
**Dependencies**: T-219, T-237
**Acceptance Criteria**:
- Backend deployed to Railway or Render
- Connected to production database
- SSL certificate configured
**Test Cases**:
- API endpoints accessible at deployed URL
- All endpoints function correctly
- Database connection established

## 3. Backend

### CLAUDE.md
File not found in backend directory.

### Models (models.py)
#### backend\src\hackathon_todo_api\models\task.py
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    user_id: str = Field(index=True)  # Changed from UUID to string to match auth system


class Task(TaskBase, table=True):
    __tablename__ = "tasks"  # Explicitly define table name

    id: Optional[int] = Field(default=None, primary_key=True)  # Changed from UUID to int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = None

#### backend\src\hackathon_todo_api\models\user.py
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid


class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False)


class User(UserBase, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.datetime.utcnow)


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

### Routes
#### backend\src\hackathon_todo_api\routes\tasks.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from ..services.task_service import (
    get_tasks, get_task_by_id, create_task, update_task,
    delete_task, toggle_task_completion
)
from ..schemas.task import TaskCreate, TaskRead, TaskUpdate, TaskToggleComplete
from ..auth.jwt import get_current_user

router = APIRouter()


@router.get("/{user_id}/tasks", response_model=List[TaskRead])
async def read_tasks(
    user_id: str,
    current_user_id: str = Depends(get_current_user)
):
    """
    Retrieve all tasks for the specified user
    """
    # Verify that the requesting user is the same as the user in the path
    if str(current_user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's tasks"
        )

    tasks = await get_tasks(current_user_id)
    return tasks


@router.post("/{user_id}/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_new_task(
    user_id: str,
    task: TaskCreate,
    current_user_id: str = Depends(get_current_user)
):
    """
    Create a new task for the specified user
    """
    # Verify that the requesting user is the same as the user in the path
    if str(current_user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create tasks for this user"
        )

    return await create_task(task, current_user_id)


@router.get("/{user_id}/tasks/{task_id}", response_model=TaskRead)
async def read_task(
    user_id: str,
    task_id: int,
    current_user_id: str = Depends(get_current_user)
):
    """
    Retrieve a specific task by ID for the specified user
    """
    # Verify that the requesting user is the same as the user in the path
    if str(current_user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's tasks"
        )

    task = await get_task_by_id(task_id, current_user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or not owned by user"
        )
    return task


@router.put("/{user_id}/tasks/{task_id}", response_model=TaskRead)
async def update_existing_task(
    user_id: str,
    task_id: int,
    task_update: TaskUpdate,
    current_user_id: str = Depends(get_current_user)
):
    """
    Update a specific task by ID for the specified user
    """
    # Verify that the requesting user is the same as the user in the path
    if str(current_user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user's tasks"
        )

    updated_task = await update_task(task_id, task_update, current_user_id)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or not owned by user"
        )
    return updated_task


@router.delete("/{user_id}/tasks/{task_id}")
async def delete_existing_task(
    user_id: str,
    task_id: int,
    current_user_id: str = Depends(get_current_user)
):
    """
    Delete a specific task by ID for the specified user
    """
    # Verify that the requesting user is the same as the user in the path
    if str(current_user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user's tasks"
        )

    deleted = await delete_task(task_id, current_user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or not owned by user"
        )
    return {"message": "Task deleted successfully"}


@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=TaskRead)
async def toggle_task_complete(
    user_id: str,
    task_id: int,
    current_user_id: str = Depends(get_current_user)
):
    """
    Toggle the completion status of a specific task for the specified user
    """
    # Verify that the requesting user is the same as the user in the path
    if str(current_user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user's tasks"
        )

    updated_task = await toggle_task_completion(task_id, current_user_id)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or not owned by user"
        )
    return updated_task

#### backend\src\hackathon_todo_api\routes\health.py
from fastapi import APIRouter
from typing import Dict

router = APIRouter()


@router.get("/health", response_model=Dict[str, str])
async def health_check():
    """
    Health check endpoint to verify API is running
    """
    return {"status": "healthy", "message": "API is running"}

#### backend\src\hackathon_todo_api\routes\auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from ..auth.jwt import create_access_token
from ..config import settings
from pydantic import BaseModel
from typing import Optional
import hashlib
import secrets
import uuid

router = APIRouter()


class UserCreate(BaseModel):
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


fake_users_db = {}  # In reality, you'd have a proper user model and database


def hash_password_with_salt(password: str) -> tuple[str, str]:
    """Generate a salt and hash the password with SHA-256"""
    salt = secrets.token_hex(32)  # Generate a random 32-byte salt
    pwdhash = hashlib.pbkdf2_hmac('sha256',
                                  password.encode('utf-8'),
                                  salt.encode('utf-8'),
                                  100000)  # Use 100,000 iterations
    pwdhash = pwdhash.hex()
    return pwdhash, salt


def verify_password(plain_password: str, hashed_password: str, salt: str) -> bool:
    """Verify a password against its hash and salt"""
    pwdhash = hashlib.pbkdf2_hmac('sha256',
                                  plain_password.encode('utf-8'),
                                  salt.encode('utf-8'),
                                  100000)
    pwdhash = pwdhash.hex()
    return pwdhash == hashed_password


def authenticate_user(email: str, password: str):
    # In a real implementation, this would query the database
    if email in fake_users_db:
        user = fake_users_db[email]
        if verify_password(password, user["hashed_password"], user["salt"]):
            return user
    return None


@router.post("/auth/register", response_model=Token)
async def register(user: UserCreate):
    """
    Register a new user
    """
    # Check if user already exists
    if user.email in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Validate email format (basic validation)
    if "@" not in user.email or "." not in user.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )

    # Validate password length
    if len(user.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters"
        )

    # Hash the password with salt
    hashed_password, salt = hash_password_with_salt(user.password)

    # Create user in "database"
    user_id = str(uuid.uuid4())
    fake_users_db[user.email] = {
        "id": user_id,
        "email": user.email,
        "hashed_password": hashed_password,
        "salt": salt
    }

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_id},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/auth/login", response_model=Token)
async def login(user_credentials: UserLogin):
    """
    Login a user and return access token
    """
    user = authenticate_user(user_credentials.email, user_credentials.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["id"]},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/auth/logout")
async def logout():
    """
    Logout a user (client-side token invalidation)
    """
    # In a real implementation, you might add the token to a blacklist
    return {"message": "Logged out successfully"}

### Database Setup
#### backend\src\hackathon_todo_api\database.py
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .config import settings

# Async engine for FastAPI application (using asyncpg driver)
import re
from sqlalchemy.dialects.postgresql import asyncpg

# Create the async database URL by replacing the protocol
async_db_url = settings.DATABASE_URL.replace('postgresql://', 'postgresql+asyncpg://', 1)

# Remove both channel_binding and sslmode from the connection string as asyncpg handles SSL differently
async_db_url = re.sub(r'[?&]sslmode=[^&]*', '', async_db_url)
async_db_url = re.sub(r'[?&]channel_binding=[^&]*', '', async_db_url)

# Clean up URL if parameters were removed from the beginning
async_db_url = async_db_url.replace('?&', '?')
if async_db_url.endswith('?') or async_db_url.endswith('&'):
    async_db_url = async_db_url.rstrip('?&')

async_engine = create_async_engine(async_db_url)

# Sync engine for Alembic migrations (using psycopg2 driver)
from sqlalchemy import create_engine
sync_engine = create_engine(settings.DATABASE_URL)

# Async session maker
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session

### Auth/Middleware
#### backend\src\hackathon_todo_api\auth\jwt.py
from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from ..config import settings
import uuid

security = HTTPBearer()


class TokenData(BaseModel):
    user_id: str


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except jwt.PyJWTError:
        raise credentials_exception
    return token_data


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    token_data = verify_token(token)

    # In a real implementation, you would fetch the user from the database
    # For now, we'll just return the user_id from the token
    return token_data.user_id

### Dependencies (pyproject.toml)
#### backend\pyproject.toml
[project]
name = "hackathon-todo-api"
version = "0.1.0"
description = "Full-stack todo application API"
authors = [{ name = "Developer", email = "dev@example.com" }]
license = { text = "MIT" }
readme = "README.md"
requires-python = ">=3.9"

dependencies = [
    "fastapi>=0.115.0",
    "uvicorn>=0.30.0",
    "sqlmodel>=0.0.22",
    "asyncpg>=0.30.0",
    "psycopg2-binary>=2.9.0",
    "pydantic>=2.9.0",
    "pydantic-settings>=2.0.0",
    "alembic>=1.13.0",
    "aiosqlite>=0.19.0",
    "pyjwt>=2.8.0",
    "better-exceptions>=0.3.0",
    "python-multipart>=0.0.20",
    "passlib[bcrypt]>=1.7.0",
    "python-jose[cryptography]>=3.3.0",
    "python-dotenv>=1.0.0",
    "emails>=0.6",
    "itsdangerous>=2.2.0",
    "jinja2>=3.1.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "httpx>=0.27.0",
    "black>=24.0.0",
    "isort>=5.0.0",
    "flake8>=7.0.0",
    "mypy>=1.0.0",
]

[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["src"]

## 4. Frontend

### CLAUDE.md
File not found in frontend directory.

### API Client
#### frontend\src\lib\api.ts
import { Task, TaskInput } from '@/types'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const getSessionData = (): { userId: string; token: string } | null => {
  if (typeof window === 'undefined') return null

  const sessionStr = localStorage.getItem('session')
  if (!sessionStr) return null

  try {
    const session = JSON.parse(sessionStr)
    const userId = session.user?.id
    const token = session.token

    if (!userId || !token) return null

    return { userId, token }
  } catch (e) {
    console.error('Failed to parse session data', e)
    return null
  }
}

const apiRequest = async <T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> => {
  const sessionData = getSessionData()

  if (!sessionData) {
    throw new Error('User not authenticated')
  }

  const { userId, token } = sessionData

  // Build URL: /api/{userId}/tasks...
  // endpoint comes in as "/tasks" or "/tasks/123" etc.
  let path = endpoint
  if (endpoint.startsWith('/tasks')) {
    path = `/${userId}/tasks` + endpoint.substring(6)
  }

  // Final URL: http://localhost:8000/api/{userId}/tasks
  const url = `${API_BASE_URL}/api${path}`

  console.log('API URL:', url) // Debug log

  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      ...options.headers,
    },
  })

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}))
    throw new Error(errorData.detail || errorData.message || `HTTP error! status: ${response.status}`)
  }

  if (response.status === 204) {
    return undefined as T
  }

  return response.json()
}

export const getTasks = async (): Promise<Task[]> => {
  return apiRequest<Task[]>('/tasks')
}

export const getTask = async (id: number): Promise<Task> => {
  return apiRequest<Task>(`/tasks/${id}`)
}

export const createTask = async (taskData: TaskInput): Promise<Task> => {
  return apiRequest<Task>('/tasks', {
    method: 'POST',
    body: JSON.stringify(taskData),
  })
}

export const updateTask = async (id: number, taskData: Partial<TaskInput>): Promise<Task> => {
  return apiRequest<Task>(`/tasks/${id}`, {
    method: 'PUT',
    body: JSON.stringify(taskData),
  })
}

export const deleteTask = async (id: number): Promise<void> => {
  await apiRequest<void>(`/tasks/${id}`, {
    method: 'DELETE',
  })
}

export const toggleTaskComplete = async (id: number): Promise<Task> => {
  return apiRequest<Task>(`/tasks/${id}/complete`, {
    method: 'PATCH',
  })
}

### Auth Setup
#### frontend\src\lib\auth.tsx
// Real authentication implementation
import { useState, useEffect, createContext, useContext } from 'react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface User {
  id: string;
  email: string;
}

interface SessionData {
  user: User | null;
  token: string | null;
}

interface SessionContextType {
  data: SessionData | null;
  status: 'loading' | 'authenticated' | 'unauthenticated';
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (email: string, password: string) => Promise<void>;
  signOut: () => void;
}

const SessionContext = createContext<SessionContextType | undefined>(undefined);

// Authentication functions
export const login = async (email: string, password: string): Promise<SessionData> => {
  try {
    const response = await fetch(`${API_URL}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || 'Login failed');
    }

    const data = await response.json();

    // Extract user ID from JWT token (the 'sub' claim in the payload)
    let userId = '';
    try {
      const tokenParts = data.access_token.split('.');
      if (tokenParts.length === 3) {
        const payload = atob(tokenParts[1]);
        const tokenPayload = JSON.parse(payload);
        userId = tokenPayload.sub || '';
      }
    } catch (e) {
      console.error('Error decoding JWT token:', e);
      throw new Error('Invalid token received from server');
    }

    const sessionData = {
      user: { id: userId, email: email },
      token: data.access_token
    };

    localStorage.setItem('session', JSON.stringify(sessionData));
    return sessionData;
  } catch (error) {
    console.error('Login failed:', error);
    throw error;
  }
};

export const signup = async (email: string, password: string): Promise<SessionData> => {
  try {
    const response = await fetch(`${API_URL}/api/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || 'Signup failed');
    }

    const data = await response.json();

    // Extract user ID from JWT token (the 'sub' claim in the payload)
    let userId = '';
    try {
      const tokenParts = data.access_token.split('.');
      if (tokenParts.length === 3) {
        const payload = atob(tokenParts[1]);
        const tokenPayload = JSON.parse(payload);
        userId = tokenPayload.sub || '';
      }
    } catch (e) {
      console.error('Error decoding JWT token:', e);
      throw new Error('Invalid token received from server');
    }

    const sessionData = {
      user: { id: userId, email: email },
      token: data.access_token
    };

    localStorage.setItem('session', JSON.stringify(sessionData));
    return sessionData;
  } catch (error) {
    console.error('Signup failed:', error);
    throw error;
  }
};

export const logout = (): void => {
  localStorage.removeItem('session');
  window.location.href = '/auth/login';
};

// Custom hook for session management
export const useSession = (): SessionContextType => {
  const context = useContext(SessionContext);
  if (context === undefined) {
    throw new Error('useSession must be used within a SessionProvider');
  }
  return context;
};

// Session provider component
export const SessionProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [sessionData, setSessionData] = useState<SessionData | null>(null);
  const [status, setStatus] = useState<'loading' | 'authenticated' | 'unauthenticated'>('loading');

  useEffect(() => {
    // Initialize session on mount
    const initSession = () => {
      try {
        const sessionStr = localStorage.getItem('session');
        if (sessionStr) {
          const session = JSON.parse(sessionStr);
          setSessionData(session);
          setStatus('authenticated');
        } else {
          setSessionData(null);
          setStatus('unauthenticated');
        }
      } catch (error) {
        console.error('Error initializing session:', error);
        setSessionData(null);
        setStatus('unauthenticated');
      }
    };

    initSession();
  }, []);

  const signIn = async (email: string, password: string) => {
    try {
      const session = await login(email, password);
      setSessionData(session);
      setStatus('authenticated');
    } catch (error) {
      throw error;
    }
  };

  const signUp = async (email: string, password: string) => {
    try {
      const session = await signup(email, password);
      setSessionData(session);
      setStatus('authenticated');
    } catch (error) {
      throw error;
    }
  };

  const signOut = () => {
    logout();
    setSessionData(null);
    setStatus('unauthenticated');
  };

  const value: SessionContextType = {
    data: sessionData,
    status,
    signIn,
    signUp,
    signOut
  };

  return (
    <SessionContext.Provider value={value}>
      {children}
    </SessionContext.Provider>
  );
};

### Dependencies (relevant from package.json)
#### frontend\package.json
{
  "name": "hackathon-todo-frontend",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "@types/node": "^22.0.0",
    "@types/react": "^19.0.0",
    "@types/react-dom": "^19.0.0",
    "autoprefixer": "^10.4.0",
    "better-auth": "^1.0.0",
    "eslint": "^9.0.0",
    "eslint-config-next": "^16.1.4",
    "next": "^16.1.4",
    "postcss": "^8.4.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "tailwindcss": "^3.4.0",
    "typescript": "^5.0.0"
  }
}

## 5. Current State Summary

### Task Model Schema
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | int | No | Primary key, auto-incrementing integer |
| user_id | str | Yes | User identifier to whom the task belongs |
| title | str | Yes | Task title (1-200 characters) |
| description | str | No | Task description (max 1000 characters) |
| completed | bool | No | Task completion status (default: False) |
| created_at | datetime | No | Timestamp when task was created |
| updated_at | datetime | No | Timestamp when task was last updated |

### API Endpoints Table
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | /api/health | No | Health check endpoint |
| POST | /api/auth/register | No | Register a new user |
| POST | /api/auth/login | No | Authenticate a user |
| POST | /api/auth/logout | No | Logout a user |
| GET | /api/{user_id}/tasks | Yes | Get user's tasks |
| POST | /api/{user_id}/tasks | Yes | Create a new task for user |
| GET | /api/{user_id}/tasks/{task_id} | Yes | Get a specific task for user |
| PUT | /api/{user_id}/tasks/{task_id} | Yes | Update a task for user |
| DELETE | /api/{user_id}/tasks/{task_id} | Yes | Delete a task for user |
| PATCH | /api/{user_id}/tasks/{task_id}/complete | Yes | Toggle task completion status |

### Tech Stack Confirmed
- Frontend: Next.js 16+, TypeScript, Tailwind CSS
- Backend: FastAPI, Python 3.9+
- Database: PostgreSQL (Neon)
- Auth: Custom JWT implementation
- ORM: SQLModel

## 6. Phase 3 Integration Points

### For MCP Server (tool operations)
- Database session pattern used: AsyncSessionLocal from SQLAlchemy with asyncpg
- CRUD function signatures: Functions in services\task_service.py using async/await with proper type hints

### For Chat Endpoint
- Existing route patterns: FastAPI routers with proper HTTP methods and status codes
- Auth verification approach: JWT token verification using get_current_user dependency with HTTPBearer scheme

### For Conversation/Message Models (to be added)
- Suggested location: backend/src/hackathon_todo_api/models/conversation.py and message.py
- Follow existing patterns from: task.py model with SQLModel and proper field validations

### Environment Variables Needed
- DATABASE_URL: PostgreSQL connection string
- SECRET_KEY: JWT secret key for token signing
- ALGORITHM: JWT algorithm (default HS256)
- ACCESS_TOKEN_EXPIRE_MINUTES: Token expiration time
- ALLOWED_ORIGINS: CORS allowed origins

## 7. Potential Issues / Notes
- The backend currently uses a fake in-memory user database (fake_users_db) which should be replaced with proper database storage
- The frontend uses localStorage for session storage which may not be ideal for security-sensitive applications
- Task IDs are integers rather than UUIDs which differs from the original spec
- The authentication system is custom-built rather than using Better Auth as originally planned in the specs
- There's a typo in main.py: ALLOWED_ORIGINS should be ALLOWED_ORIGINS (missing 'G')