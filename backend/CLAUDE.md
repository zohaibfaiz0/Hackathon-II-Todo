# Backend Guidelines

## Stack
- FastAPI (async Python web framework)
- SQLModel (ORM combining SQLAlchemy + Pydantic)
- Neon PostgreSQL (serverless Postgres)
- JWT Authentication (PyJWT)
- Password Hashing (passlib with bcrypt)

## Project Structure
```
backend/src/hackathon_todo_api/
├── main.py           # FastAPI app entry point, CORS, routers
├── config.py         # Pydantic Settings (env vars)
├── database.py       # Async SQLAlchemy engine, session maker
├── models/           # SQLModel database models
│   ├── task.py       # Task model
│   └── user.py       # User model
├── schemas/          # Pydantic request/response schemas
│   └── task.py
├── routes/           # API route handlers
│   ├── auth.py       # /api/auth/* endpoints
│   ├── health.py     # /api/health endpoint
│   └── tasks.py      # /api/{user_id}/tasks/* endpoints
├── services/         # Business logic layer
│   ├── task_service.py
│   └── user_service.py
└── auth/
    └── jwt.py        # JWT token creation/verification
```

## API Conventions
- Base path: `/api/`
- Auth endpoints: `/api/auth/register`, `/api/auth/login`, `/api/auth/logout`
- User-scoped endpoints: `/api/{user_id}/tasks`
- All task endpoints require JWT Bearer token
- User can only access their own tasks (validated by comparing token user_id with URL user_id)

## Database
- Async sessions via `AsyncSessionLocal`
- Connection string from `DATABASE_URL` env var
- Migrations via Alembic: `uv run alembic upgrade head`

## Authentication Flow
1. User registers/logs in → receives JWT token
2. Token contains `sub` claim with user ID (as string)
3. Frontend stores token, sends in `Authorization: Bearer <token>` header
4. Backend `get_current_user` dependency extracts and validates token
5. Routes compare URL `user_id` with token `user_id` for authorization

## Running Locally
```bash
cd backend
uv sync
uv run alembic upgrade head
uv run uvicorn src.hackathon_todo_api.main:app --reload --port 8000
```

## Testing
```bash
cd backend
uv run pytest
```

## Phase III: Chat Components

### New Directories
- `agents/` - AI agent configuration and processing
- `tools/` - MCP-style tool definitions for OpenAI function calling

### Chat-Related Files
| File | Purpose |
|------|---------|
| `models/conversation.py` | Conversation SQLModel |
| `models/message.py` | Message SQLModel |
| `schemas/chat.py` | ChatRequest, ChatResponse, ToolCallInfo |
| `routes/chat.py` | POST /api/{user_id}/chat endpoint |
| `services/chat_service.py` | Chat business logic, conversation management |
| `agents/todo_agent.py` | OpenAI integration, tool execution |
| `tools/todo_tools.py` | Task management tool definitions |

### Chat Endpoint
```
POST /api/{user_id}/chat
Authorization: Bearer <token>

Request:
{
  "conversation_id": 123,  // optional
  "message": "Add a task to buy groceries"
}

Response:
{
  "conversation_id": 123,
  "response": "I've added 'Buy groceries' to your tasks!",
  "tool_calls": [...]
}
```

### MCP-Style Tools
The AI agent has access to these tools:
- `add_task` - Create new tasks
- `list_tasks` - List tasks (all/pending/completed)
- `complete_task` - Mark task as complete
- `delete_task` - Remove a task
- `update_task` - Modify task title/description

### Environment Variables (Phase III)
```
OPENAI_API_KEY=sk-...  # Required for chat functionality
```