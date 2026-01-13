---
id: 1
title: Update Project Constitution
stage: constitution
date: 2026-01-13
surface: agent
model: claude-opus-4-5-20251101
feature: none
branch: master
user: AA
command: sp.constitution
labels: [constitution, setup, governance]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
---

## Prompt

```
# CONSTITUTION: Evolution of Todo - Hackathon II

## 1. PROJECT IDENTITY

### 1.1 Mission
Build "The Evolution of Todo" - a spec-driven application evolving from Python console app (Phase I) to full-stack web application (Phase II), demonstrating mastery of Spec-Driven Development.

### 1.2 The Prime Directive
**"No Task = No Code."**

All agents must follow the Spec-Kit Plus lifecycle:
1. **Specify** → Requirements in `speckit.specify`
2. **Plan** → Architecture in `speckit.plan`
3. **Tasks** → Atomic work units in `speckit.tasks`
4. **Implement** → Code only after Task ID exists

*Any code without a referenced Task ID is a critical failure.*

### 1.3 Success Criteria
- Zero manual code writing - all generated from specs
- Zero runtime errors on first deployment
- 100% type coverage (Python & TypeScript)
- All 5 Basic Level features functional per phase

---

## 2. ARCHITECTURAL PRINCIPLES

### 2.1 Core Rules

| Principle | Enforcement |
|-----------|-------------|
| Single Responsibility | Max 200 lines per file |
| Separation of Concerns | UI, Logic, Data strictly isolated |
| Fail Fast | Validate all inputs at boundaries |
| Explicit over Implicit | No magic, full type hints everywhere |
| Dependency Inversion | Depend on abstractions, not concretions |

### 2.2 Layered Architecture

```
PRESENTATION → APPLICATION → DOMAIN → INFRASTRUCTURE
```

- **Presentation:** CLI (Phase I) / Next.js (Phase II)
- **Application:** Service functions / FastAPI routes
- **Domain:** Models, business rules, validation (pure logic)
- **Infrastructure:** Storage implementations

*Constraint: Lower layers NEVER import from upper layers.*

### 2.3 Phase Transition Principle
- Domain layer must remain portable across phases
- Use abstractions (interfaces) for infrastructure
- Phase II extends Phase I, never rewrites

---

## 3. TECHNOLOGY STACK

### 3.1 Phase I: Console Application

| Component | Technology | Mandatory |
|-----------|------------|-----------|
| Runtime | Python 3.13+ | YES |
| Package Manager | UV | YES |
| Type Checking | mypy (strict) | YES |
| Linting/Format | ruff | YES |

### 3.2 Phase II: Full-Stack Web

| Layer | Technology | Mandatory |
|-------|------------|-----------|
| Frontend | Next.js 16+ (App Router) | YES |
| Frontend Lang | TypeScript 5+ (strict) | YES |
| Styling | Tailwind CSS | YES |
| Backend | FastAPI 0.115+ | YES |
| ORM | SQLModel (async) | YES |
| Database | Neon Serverless PostgreSQL | YES |
| Authentication | Better Auth (JWT) | YES |

### 3.3 Prohibited
- Django, Flask, Express
- Redux, Zustand, MobX
- CSS-in-JS (styled-components, emotion)
- Raw SQL strings
- Synchronous database drivers

---

## 4. CODING STANDARDS

### 4.1 Python
- All files start with `from __future__ import annotations`
- Google-style docstrings for all public functions
- Custom exception hierarchy (never bare `Exception`)
- Naming: `snake_case` functions, `PascalCase` classes
- No mutable default arguments

### 4.2 TypeScript
- Strict mode enabled, no `any` type
- Server Components by default, Client only when needed
- Tailwind classes only, no inline styles
- Props always typed with interfaces

### 4.3 Universal
- Maximum function length: 50 lines
- Maximum file length: 200 lines
- All public APIs documented
- No commented-out code committed

---

## 5. DATA INTEGRITY

### 5.1 Task Entity Rules
- Title: Required, 1-200 characters
- Description: Optional, max 1000 characters
- Completed: Boolean, defaults to false
- Timestamps: Auto-generated, never user-provided

### 5.2 Validation Strategy
- Validate at domain layer (single source of truth)
- Reject invalid data immediately (fail fast)
- Return specific error codes, not generic messages

### 5.3 User Data Isolation (Phase II)
- Users may only access their own tasks
- Every query filtered by authenticated user_id
- No admin/superuser bypass in MVP

---

## 6. SECURITY REQUIREMENTS

### 6.1 Authentication (Phase II)
- All API endpoints require JWT (except health check)
- Token verification on every request
- URL user_id must match token user_id

### 6.2 Data Protection
- No secrets in code (use environment variables)
- No sensitive data in logs
- Input sanitization at all boundaries

### 6.3 Forbidden Practices
- Hardcoded credentials
- SQL string concatenation
- `eval()` or `exec()`
- Disabled type checking (`# type: ignore`)

---

## 7. QUALITY REQUIREMENTS

### 7.1 Testing
- Domain/Models: 100% coverage
- Services: 90% coverage
- API Routes: 85% coverage
- Test naming: `test_<action>_<condition>_<result>`

### 7.2 Error Handling
- Custom exception classes for each error type
- User-friendly messages in responses
- Stack traces only in development mode

### 7.3 Documentation
- README.md with setup instructions
- CLAUDE.md with agent context
- Docstrings on all public interfaces

---

## 8. VERSION CONTROL

### 8.1 Commits
- Conventional Commits format: `type(scope): message`
- Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`
- Atomic commits (one logical change per commit)

### 8.2 Branches
- `main`: Production-ready code only
- `phase/N`: Phase development branches
- `feat/name`: Feature branches

---

## 9. AGENT BEHAVIOR RULES

### 9.1 Before Writing Code
1. Verify spec exists for the feature
2. Verify Task ID is assigned
3. Verify architecture is defined in plan

### 9.2 While Writing Code
1. Reference Task ID in comments
2. Follow layered architecture strictly
3. Use only approved technologies
4. Include type hints on everything

### 9.3 Refusal Conditions
Agent must STOP and request clarification if:
- No spec exists for requested feature
- Technology not in approved list
- Architecture violates layer boundaries
- Security requirement would be violated

### 9.4 Forbidden Actions
- Writing code without Task reference
- Using `any` type or skipping type hints
- Catching generic `Exception`
- Creating files outside defined structure
- Mixing concerns between layers

---

## 10. FEATURE REQUIREMENTS

### 10.1 Phase I: Console App (Basic Level)
1. Add Task - Create new todo items
2. Delete Task - Remove tasks from list
3. Update Task - Modify existing task details
4. View Task List - Display all tasks
5. Mark as Complete - Toggle task completion

### 10.2 Phase II: Web App (Basic Level + Auth)
1. All Phase I features as REST API
2. User signup/signin (Better Auth)
3. User-specific task isolation
4. Responsive web interface

---

**END OF CONSTITUTION**

*Version: 1.0.0*
*Scope: Phase I & Phase II*
*Authority: This document governs all development decisions.*
```

## Response snapshot

Updated the project constitution file (.specify/memory/constitution.md) with the complete "Evolution of Todo - Hackathon II" constitution as provided. The constitution establishes the foundational principles, technology stack, coding standards, and behavioral rules that will govern all development activities for this project. It emphasizes the "No Task = No Code" prime directive, layered architecture, and spec-driven development approach.

## Outcome

- ✅ Impact: Updated core governance document establishing project principles and guidelines
- 🧪 Tests: No tests affected
- 📁 Files: 1 file updated (.specify/memory/constitution.md)
- 🔁 Next prompts: Will proceed with feature specification and planning as per constitution
- 🧠 Reflection: Constitution provides strong foundation for spec-driven development approach

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - Constitution properly established
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin feature specification per constitution guidelines