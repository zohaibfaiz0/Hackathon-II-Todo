# Hackathon Todo – Full-Stack Web Application (Phase I & II)

## Phase I: Console Application
A Python-based console todo application built as **Phase I** of
**"The Evolution of Todo – Hackathon II"**.
The project focuses on spec-driven development, clean architecture, and an interactive CLI experience.

---

## Phase II: Full-Stack Web Application
This project transforms the console application into a multi-user web application with persistent storage.

### Tech Stack

- **Frontend**: Next.js 16+, TypeScript, Tailwind CSS
- **Backend**: FastAPI, SQLModel, PostgreSQL
- **Authentication**: Better Auth with JWT
- **Database**: Neon PostgreSQL

---

## Features (Phase I)

- Add tasks with a title and optional description
- View all tasks in a formatted table
- Filter tasks by status (pending / completed)
- Update existing tasks
- Delete tasks
- Mark tasks as complete or incomplete
- Interactive shell mode with persistent session

---

## Features (Phase II)

- User registration and authentication
- Create, read, update, and delete tasks
- Task completion toggling
- User data isolation
- Responsive web interface
- API documentation

---

## Prerequisites

- Python **3.13+**
- **uv** package manager
- Node.js 18+
- PostgreSQL (or access to Neon PostgreSQL)

---

## Installation

### Phase I (Console App)
```bash
git clone <repository-url>
cd hackathon-todo
uv sync
```

### Phase II (Web App)
```bash
# Backend
cd backend
pip install uv
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install --system -e .

# Frontend
cd frontend
npm install
```

---

## Quick Start

### Phase I: Interactive Shell (Recommended)

```bash
uv run python -m hackathon_todo shell
```

Example session:

```
> add "Buy groceries" --description "Milk, eggs, bread"
Task created successfully (ID: 1)

> add "Call mom"
Task created successfully (ID: 2)

> list
┌────┬───────────────┬───────────┬─────────────────────┐
│ ID │ Title         │ Status    │ Created             │
├────┼───────────────┼───────────┼─────────────────────┤
│ 1  │ Buy groceries │ Pending   │ 2025-01-13 10:30    │
│ 2  │ Call mom      │ Pending   │ 2025-01-13 10:31    │
└────┴───────────────┴───────────┴─────────────────────┘

> complete 1
Task marked as complete

> list --status completed
┌────┬───────────────┬───────────┬─────────────────────┐
│ ID │ Title         │ Status    │ Created             │
├────┼───────────────┼───────────┼─────────────────────┤
│ 1  │ Buy groceries │ Done      │ 2025-01-13 10:30    │
└────┴───────────────┴───────────┴─────────────────────┘

> exit
Goodbye!
```

---

### Phase II: Web Application

#### Backend Setup
```bash
# Navigate to the backend directory
cd backend

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies using uv
pip install uv
uv pip install --system -e .

# Create a .env file with your configuration
cp .env.example .env
# Edit .env with your database URL and secret key

# Run database migrations
alembic upgrade head

# Run the backend
uvicorn src.hackathon_todo_api.main:app --reload
```

#### Frontend Setup
```bash
# Navigate to the frontend directory
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env.local
# Edit .env.local with your backend URL

# Run the frontend
npm run dev
```

---

## Command Reference (Phase I)

| Command    | Usage                                               | Description             |
| ---------- | --------------------------------------------------- | ----------------------- |
| shell      | `shell`                                             | Start interactive shell |
| add        | `add "Title" [--description "Desc"]`                | Create a task           |
| list       | `list [--status pending\|completed]`                | List tasks              |
| view       | `view <id>`                                         | View task details       |
| update     | `update <id> [--title "New"] [--description "New"]` | Update a task           |
| complete   | `complete <id>`                                     | Mark task as completed  |
| uncomplete | `uncomplete <id>`                                   | Mark task as pending    |
| delete     | `delete <id>`                                       | Delete a task           |

---

## API Endpoints (Phase II)

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login a user
- `POST /api/auth/logout` - Logout a user

### Tasks
- `GET /api/tasks` - Get all user tasks
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{id}` - Get a specific task
- `PUT /api/tasks/{id}` - Update a task
- `DELETE /api/tasks/{id}` - Delete a task
- `PATCH /api/tasks/{id}/complete` - Toggle task completion

### Chat
- `POST /api/{user_id}/chat` - Send a chat message and get AI response

---

## Phase III: AI-Powered Todo Chatbot

Phase III adds an AI-powered chatbot interface for managing todos through natural language.

### Features
- Natural language task management ("Add a task to buy groceries")
- Conversational interface with persistent history
- AI-powered intent recognition using OpenAI
- Real-time task operations via chat

### Chat Commands Examples
| You Say | What Happens |
|---------|--------------|
| "Add a task to buy groceries" | Creates a new task |
| "Show my tasks" | Lists all your tasks |
| "What's pending?" | Lists incomplete tasks |
| "Mark task 3 as complete" | Completes the task |
| "Delete task 2" | Removes the task |
| "Change task 1 to 'Call mom'" | Updates the task |

### Additional Setup for Phase III

#### Environment Variables
Add to `backend/.env`:
```
OPENAI_API_KEY=sk-your-openai-api-key-here
```

Get your API key from: https://platform.openai.com/api-keys

#### Database Migration
```bash
cd backend
uv run alembic upgrade head
```

This creates the `conversations` and `messages` tables.

### Running Phase III

1. **Start Backend** (with OpenAI key configured):
```bash
cd backend
uv run uvicorn src.hackathon_todo_api.main:app --reload --port 8000
```

2. **Start Frontend**:
```bash
cd frontend
npm run dev
```

3. **Use the Chat**:
   - Log in to the dashboard
   - Click the chat button (bottom-right corner)
   - Start chatting with your AI todo assistant!

### Tech Stack (Phase III Additions)
- OpenAI API (Chat Completions with Function Calling)
- Custom MCP-style tools for task operations
- Real-time chat UI components

---

## Project Structure

```
hackathon-todo/
├── frontend/                 # Next.js application
│   ├── src/
│   │   ├── app/             # App Router pages
│   │   ├── components/      # Reusable components
│   │   ├── lib/             # Utilities and API clients
│   │   └── types/           # TypeScript definitions
│   └── package.json
├── backend/                  # FastAPI application
│   ├── src/
│   │   └── hackathon_todo_api/
│   │       ├── models/      # Database models
│   │       ├── schemas/     # Pydantic schemas
│   │       ├── routes/      # API routes
│   │       ├── services/    # Business logic
│   │       └── auth/        # Authentication utilities
│   ├── alembic/             # Database migrations
│   └── pyproject.toml
├── specs/                   # Specifications for both phases
│   └── phase-ii-full-stack-web-app/
│       ├── spec.md          # Phase II requirements
│       ├── plan.md          # Phase II architecture
│       └── tasks.md         # Phase II implementation tasks
├── src/                     # Phase I source code
├── tests/                   # Phase I tests
├── docker-compose.yml       # Docker configuration
├── pyproject.toml           # Phase I dependencies
├── README.md                # This file
└── uv.lock                  # Lock file
```

---

## Architecture Overview (Phase I)

```
PRESENTATION   : CLI (Click + Rich)
APPLICATION    : TaskService
DOMAIN         : Task model, validation, exceptions
INFRASTRUCTURE : In-memory storage
```

---

## Architecture Overview (Phase II)

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

---

## Development

### Phase I Development
```bash
# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src/hackathon_todo

# Type checking
uv run mypy src/

# Linting
uv run ruff check src/
```

### Phase II Development
The backend uses FastAPI which provides automatic API documentation at `http://localhost:8000/docs`.
The frontend uses Next.js App Router. Pages are organized in the `src/app` directory.

---

## Running with Docker

Alternatively, you can run the entire application using Docker:

```bash
# Build and start all services
docker-compose up --build

# Run in detached mode
docker-compose up -d --build
```

---

## Spec-Driven Development

This project follows **Spec-Kit Plus** methodology:

* `specs/phase-ii-full-stack-web-app/spec.md` – Phase II Requirements
* `specs/phase-ii-full-stack-web-app/plan.md` – Phase II Architecture plan
* `specs/phase-ii-full-stack-web-app/tasks.md` – Phase II Task breakdown

Original Phase I specs:
* `specs/todo-console-app/spec.md` – Phase I Requirements
* `specs/todo-console-app/plan.md` – Phase I Architecture plan
* `specs/todo-console-app/tasks.md` – Phase I Task breakdown


## Phase III: AI-Powered Todo Chatbot
Adds an AI chatbot interface for managing tasks via natural language using Google Gemini.

### Features
- **Natural Language**: "Add a task to buy groceries"
- **Context Aware**: "Delete the last task I added"
- **Tool Calling**: AI executes database operations directly
- **Tech Stack**: Google Gemini API, Custom Tool Schema, React Chat UI

### Environment Variables
Add to `backend/.env`:
```
GEMINI_API_KEY=your-gemini-api-key
```

---

## Phase IV: Kubernetes Deployment
Containerizes the application and deploys it to a local Kubernetes cluster using Helm.

### Tech Stack
- **Containerization**: Docker (Multi-stage builds)
- **Orchestration**: Kubernetes (Minikube)
- **Config Management**: Helm Charts

### Features
- Production-ready Docker images (`python:3.12-slim`, `node:20-alpine`)
- StatefulSet for PostgreSQL persistence
- Secrets management for API keys
- Automated deployment script

### Quick Deploy (Local)
```bash
cd deploy
bash local-setup.sh
```
*This builds images inside Minikube and deploys the Helm chart.*

---

## Phase V: Advanced Cloud Architecture
Adds Event-Driven Architecture and Distributed Application Runtime (Dapr).

### Architecture
- **Event Bus**: Redpanda (Kafka-compatible)
- **Runtime**: Dapr (Sidecars)
- **Pattern**: Pub/Sub (Publish-Subscribe)

### Features
- **Event Logging**: Backend publishes `task.created` events to Redpanda via Dapr.
- **Service Invocation**: Frontend communicates with Backend via Dapr sidecars.
- **Resilience**: Retries, circuit breaking, and observability provided by Dapr.

### Deployment Note
Phase 5 code is fully implemented in the repository. However, for local demonstrations on resource-constrained environments (like standard laptops), the "Heavy" features (Redpanda/Dapr sidecars) are disabled by default in `values.yaml` to ensure stability.

To enable full Phase 5 features, set `redpanda.enabled: true` in `deploy/k8s/helm/todo-app/values.yaml`.

---

## Project Structure

```
hackathon-todo/
├── frontend/                 # Next.js application
│   ├── src/
│   │   ├── app/             # Pages & Chat Integration
│   │   ├── components/      # UI Components (ChatWindow, etc.)
│   │   ├── lib/             # API Clients (Standard & Dapr)
├── backend/                  # FastAPI application
│   ├── src/
│   │   └── hackathon_todo_api/
│   │       ├── agents/      # AI Agents (Gemini)
│   │       ├── tools/       # Tool definitions
│   │       ├── services/    # Business logic (with Event Publishing)
│   │       ├── routes/      # API endpoints (including Event Subscriber)
├── deploy/                   # Infrastructure
│   ├── k8s/helm/todo-app/   # Main Helm Chart
│   │   ├── templates/       # K8s Manifests
│   │   │   ├── components/  # Dapr Components (PubSub)
│   └── local-setup.sh       # Automation script
├── specs/                    # Spec-Driven Development Artifacts
│   ├── phase-ii-.../
│   ├── phase-iii-.../
│   ├── phase-iv-.../
│   └── phase-v-.../
```

---

## Running with Docker (Simple)

To run without Kubernetes:

```bash
docker-compose up --build
```

---

## License
MIT License
```