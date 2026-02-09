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
RUN uv sync --frozen --no-dev --no-install-project

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