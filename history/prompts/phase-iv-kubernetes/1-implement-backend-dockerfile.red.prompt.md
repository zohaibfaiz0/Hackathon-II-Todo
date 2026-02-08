---
id: 1
title: Implement backend Dockerfile multi-stage build
stage: red
date: 2026-02-07
surface: agent
model: claude-sonnet-4-5
feature: phase-iv-kubernetes
branch: main
user:
command: sp.implement
labels: [docker, backend, implementation]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - backend/Dockerfile
tests:
---

## Prompt

# Implement T-401: Create Backend Dockerfile

## Task
Create a production-ready Dockerfile for the FastAPI backend.

## File Location
`backend/Dockerfile`

## Requirements
- **Base Image:** `python:3.12-slim` (compatible with `uv`)
- **Build Strategy:** Multi-stage (builder + runner)
- **Dependency Manager:** `uv`
- **Port:** Expose 8000
- **User:** Non-root user for security

## Content to Write

```dockerfile
# Stage 1: Builder
FROM python:3.12-slim AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies into a virtual environment
# --no-dev: Production dependencies only
# --frozen: Require uv.lock to match pyproject.toml
RUN uv sync --frozen --no-dev

# Stage 2: Runner
FROM python:3.12-slim AS runner

# Create a non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory
WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy source code
COPY src ./src
COPY alembic.ini ./
COPY alembic ./alembic

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "src.hackathon_todo_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Verification Command
Run this after creating the file to ensure it builds:
```bash
docker build -t todo-backend ./backend
```

## Response snapshot

Created a production-ready multi-stage Dockerfile for the FastAPI backend that:
- Uses python:3.12-slim base image
- Implements proper multi-stage build pattern with builder and runner stages
- Uses uv for dependency management
- Creates a non-root user for security
- Exposes port 8000 as required
- Sets appropriate environment variables
- Has the correct CMD to run the application

## Outcome

- ✅ Impact: Successfully created production-ready backend Dockerfile with multi-stage build
- 🧪 Tests: Unable to test build due to Docker Desktop not running
- 🗁 Files: Updated backend/Dockerfile with multi-stage build pattern
- 🔄 Next prompts: Implement frontend Dockerfile, configure Helm charts
- 🧠 Reflection: Multi-stage build properly separates build-time and runtime dependencies for security and optimization

## Evaluation notes (flywheel)

- Failure modes observed: Docker Desktop not running prevented build verification
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test Docker build once Docker Desktop is running