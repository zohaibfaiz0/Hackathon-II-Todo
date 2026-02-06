# Phase III: AI-Powered Todo Chatbot - Architecture Plan

## 1. Executive Summary

This document outlines the architectural plan for implementing an AI-powered chatbot interface for managing todos through natural language. The solution will integrate OpenAI's technology with the existing task management system to allow users to manage their tasks conversationally. The system will maintain the stateless architecture principle and seamlessly integrate with the existing Phase II functionality while extending capabilities with AI-driven task management.

## 2. Architecture Overview

### 2.1 High-Level Architecture
```
┌─────────────────┐     ┌──────────────────────────────────────────────┐     ┌─────────────────┐
│                 │     │ FastAPI Server                               │     │                 │
│ Chat UI         │     │ ┌────────────────────────────────────────┐   │     │ Neon DB         │
│ (Frontend)      │────▶│ │ POST /api/{user_id}/chat               │   │     │ (PostgreSQL)    │
│                 │     │ └───────────────┬────────────────────────┘   │     │                 │
│                 │     │                 │                            │     │ - tasks         │
│                 │     │                 ▼                            │     │ - users         │
│                 │     │ ┌────────────────────────────────────────┐   │     │ - conversations │
│                 │◀────│ │ OpenAI Client (Chat Completions)     │   │     │ - messages      │
│                 │     │ └───────────────┬────────────────────────┘   │     │                 │
│                 │     │                 │                            │     │                 │
│                 │     │                 ▼                            │     │                 │
│                 │     │ ┌────────────────────────────────────────┐   │────▶│                 │
│                 │     │ │ Tool Functions (MCP-style)            │   │◀────│                 │
│                 │     │ └────────────────────────────────────────┘   │     │                 │
└─────────────────┘     └──────────────────────────────────────────────┘     └─────────────────┘
```

### 2.2 Request Flow Diagram
```
1. User types message in ChatInput component
2. Frontend calls POST /api/{user_id}/chat with message and conversation_id (if exists)
3. Auth middleware validates JWT token and extracts user_id
4. ChatService validates request and loads conversation history
5. System calls OpenAI Chat Completions API with conversation history and tools
6. OpenAI processes message and determines appropriate tool(s) to call
7. Tool functions execute against existing TaskService
8. Tool results are processed and sent back to OpenAI
9. OpenAI generates natural language response
10. ChatService saves user and assistant messages to database
11. Response is returned to frontend
12. Frontend displays response in chat window
```

## 3. New File Structure

Document ONLY new files to add (no modifications to existing):

```
backend/src/hackathon_todo_api/
├── models/
│   ├── conversation.py      # NEW
│   └── message.py           # NEW
├── schemas/
│   └── chat.py              # NEW
├── routes/
│   └── chat.py              # NEW
├── services/
│   └── chat_service.py      # NEW
├── tools/                    # NEW directory (replacing MCP concept)
│   ├── __init__.py
│   └── todo_tools.py
└── agents/                   # NEW directory
    ├── __init__.py
    └── todo_agent.py

frontend/src/
├── components/
│   └── chat/                 # NEW directory
│       ├── ChatWindow.tsx
│       ├── ChatMessage.tsx
│       ├── ChatInput.tsx
│       └── index.ts
├── lib/
│   └── chat.ts              # NEW
└── types/
    └── chat.ts              # NEW
```

## 4. Technology Decisions

### 4.1 OpenAI Integration
- **Package**: `openai>=1.0.0`
- **Approach**: Use OpenAI Chat Completions API with function calling capabilities (not full Agents SDK, which is overkill)
- **Function Calling**: Define tool schemas in JSON format that map to our backend functions
- **Async Considerations**: Use async/await pattern consistent with FastAPI and existing async SQLAlchemy

### 4.2 Tool Implementation (Replacing MCP Concept)
After research, the MCP (Model Context Protocol) SDK is not yet widely available or stable. Instead, we'll implement the tools as function definitions passed to OpenAI's Chat Completions API:

- Tools will be defined as Python functions in `todo_tools.py`
- These functions will be converted to JSON schemas compatible with OpenAI's function calling
- The functions will call the existing task_service functions
- This approach provides the same functionality as MCP without requiring experimental tools

### 4.3 Frontend Chat Interface
Since OpenAI's ChatKit requires their proprietary backend services, we'll implement a custom chat UI component using React and Tailwind CSS:
- Custom implementation provides more control and flexibility
- Will match the existing dashboard design language
- Built with TypeScript for type safety
- Compatible with existing auth and state management patterns

## 5. Detailed Component Design

### 5.1 Database Models

**Conversation Model** (following existing SQLModel patterns):
```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Message Model**:
```python
class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    user_id: str = Field(index=True)
    role: str  # "user" or "assistant"
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    # Optional: tool_calls field if we need to store which tools were called
```

### 5.2 Pydantic Schemas

```python
from pydantic import BaseModel, Field
from typing import Optional, List, Any

class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None
    message: str = Field(min_length=1, max_length=2000)

class ToolCallInfo(BaseModel):
    tool: str
    arguments: dict
    result: dict

class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: List[ToolCallInfo] = []
```

### 5.3 Tool Functions Design

For each tool, we'll define functions with corresponding JSON schemas:
```python
async def add_task_tool(user_id: str, title: str, description: Optional[str] = None) -> dict:
    """Create a new task for the user."""
    try:
        from ..services.task_service import create_task
        from ..schemas.task import TaskCreate

        task = await create_task(
            TaskCreate(title=title, description=description or ""),
            user_id
        )
        return {"task_id": task.id, "status": "created", "title": task.title}
    except Exception as e:
        return {"error": str(e), "status": "failed"}

# Define similar functions for list_tasks, complete_task, delete_task, update_task
```

The tool schemas for OpenAI will be:
```python
ADD_TASK_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "add_task",
        "description": "Create a new task for the user",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "The task title"},
                "description": {"type": "string", "description": "The task description"}
            },
            "required": ["title"]
        }
    }
}
```

### 5.4 Agent Configuration

The agent will be implemented as a function in the agents module that orchestrates the conversation:
```python
from openai import AsyncOpenAI
from ..config import settings

class TodoAgent:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def process_message(self, messages: List[dict], tools: List[dict]) -> str:
        response = await self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        return response.choices[0].message
```

### 5.5 ChatService Design

```python
from ..database import AsyncSessionLocal
from ..models.conversation import Conversation
from ..models.message import Message
from .todo_agent import TodoAgent
from .todo_tools import get_all_tools

class ChatService:
    def __init__(self):
        self.agent = TodoAgent()

    async def create_conversation(self, user_id: str) -> Conversation:
        async with AsyncSessionLocal() as session:
            conversation = Conversation(user_id=user_id)
            session.add(conversation)
            await session.commit()
            await session.refresh(conversation)
            return conversation

    async def get_conversation(self, conversation_id: int, user_id: str) -> Optional[Conversation]:
        async with AsyncSessionLocal() as session:
            statement = select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            )
            result = await session.execute(statement)
            return result.scalar_one_or_none()

    async def add_message(self, conversation_id: int, user_id: str, role: str, content: str) -> Message:
        async with AsyncSessionLocal() as session:
            message = Message(
                conversation_id=conversation_id,
                user_id=user_id,
                role=role,
                content=content
            )
            session.add(message)
            await session.commit()
            await session.refresh(message)
            return message

    async def get_messages(self, conversation_id: int, limit: int = 20) -> List[Message]:
        async with AsyncSessionLocal() as session:
            statement = select(Message).where(
                Message.conversation_id == conversation_id
            ).order_by(Message.created_at.desc()).limit(limit)
            result = await session.execute(statement)
            messages = result.scalars().all()
            return list(reversed(messages))  # Return in chronological order

    async def process_chat(self, user_id: str, message: str, conversation_id: Optional[int] = None) -> ChatResponse:
        # Create or retrieve conversation
        if conversation_id is None:
            conversation = await self.create_conversation(user_id)
            conversation_id = conversation.id
        else:
            conversation = await self.get_conversation(conversation_id, user_id)
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")

        # Save user message
        await self.add_message(conversation_id, user_id, "user", message)

        # Get conversation history
        history = await self.get_messages(conversation_id)
        messages = [{"role": msg.role, "content": msg.content} for msg in history]

        # Process with AI
        tools = get_all_tools()
        ai_response = await self.agent.process_message(messages, tools)

        # Handle tool calls if any
        tool_calls = []
        if ai_response.tool_calls:
            for tool_call in ai_response.tool_calls:
                tool_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                # Execute the appropriate tool function
                result = await execute_tool(tool_name, user_id, **arguments)
                tool_calls.append({
                    "tool": tool_name,
                    "arguments": arguments,
                    "result": result
                })

        # Save AI response
        await self.add_message(conversation_id, user_id, "assistant", ai_response.content)

        return ChatResponse(
            conversation_id=conversation_id,
            response=ai_response.content,
            tool_calls=tool_calls
        )
```

### 5.6 Chat Route Design

```python
from fastapi import APIRouter, Depends, HTTPException
from ..services.chat_service import ChatService
from ..schemas.chat import ChatRequest, ChatResponse
from ..auth.jwt import get_current_user

router = APIRouter()
chat_service = ChatService()

@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: str,
    request: ChatRequest,
    current_user_id: str = Depends(get_current_user)
):
    # Validate user authorization
    if str(current_user_id) != user_id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access this conversation"
        )

    # Process message through ChatService
    response = await chat_service.process_chat(
        user_id=user_id,
        message=request.message,
        conversation_id=request.conversation_id
    )

    return response
```

## 6. Frontend Component Design

### 6.1 TypeScript Types
```typescript
export interface ChatMessage {
  id: number;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  toolCalls?: ToolCall[];
}

export interface ToolCall {
  tool: string;
  arguments: Record<string, any>;
  result: Record<string, any>;
}

export interface ChatResponse {
  conversation_id: number;
  response: string;
  tool_calls: ToolCall[];
}

export interface Conversation {
  id: number;
  created_at: string;
  updated_at: string;
}
```

### 6.2 API Client Functions
```typescript
// frontend/src/lib/chat.ts
import { ChatResponse } from '@/types/chat';

export const sendChatMessage = async (
  userId: string,
  message: string,
  conversationId?: number
): Promise<ChatResponse> => {
  const sessionData = getSessionData();
  if (!sessionData) {
    throw new Error('User not authenticated');
  }

  const { token } = sessionData;

  const response = await fetch(`${API_BASE_URL}/api/${userId}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify({
      conversation_id: conversationId,
      message
    }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || errorData.message || `HTTP error! status: ${response.status}`);
  }

  return response.json();
}
```

### 6.3 Component Props Interfaces
```typescript
interface ChatMessageProps {
  message: ChatMessage;
}

interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
  placeholder?: string;
}

interface ChatWindowProps {
  initialConversationId?: number;
}
```

### 6.4 ChatWindow State Management
```typescript
interface ChatWindowState {
  messages: ChatMessage[];
  conversationId: number | null;
  isLoading: boolean;
  error: string | null;
}
```

## 7. Integration Strategy

### 7.1 Backend Integration Points
| Existing Code | How Phase 3 Uses It |
|---------------|---------------------|
| task_service.create_task() | Called by add_task_tool function |
| task_service.get_tasks() | Called by list_tasks_tool function |
| task_service.toggle_task_completion() | Called by complete_task_tool function |
| task_service.delete_task() | Called by delete_task_tool function |
| task_service.update_task() | Called by update_task_tool function |
| get_current_user dependency | Used in chat route for auth |
| AsyncSessionLocal | Used in ChatService for DB operations |
| Settings from config.py | Access to OPENAI_API_KEY |

### 7.2 Frontend Integration Points
| Existing Code | How Phase 3 Uses It |
|---------------|---------------------|
| getSessionData() from api.ts | Pattern reused in chat.ts |
| useSession() from auth.tsx | Used in ChatWindow for auth state |
| Dashboard page | Chat UI added as integrated component |

### 7.3 Files to Modify (MINIMAL CHANGES ONLY)
| File | Change |
|------|--------|
| backend/src/hackathon_todo_api/main.py | Add: `from .routes import chat` and `app.include_router(chat.router, ...)` |
| backend/src/hackathon_todo_api/models/__init__.py | Add: exports for Conversation, Message |
| backend/src/hackathon_todo_api/config.py | Add: `OPENAI_API_KEY: str` |
| backend/.env.example | Add: `OPENAI_API_KEY=` |
| frontend/src/app/dashboard/page.tsx | Add: Chat integration component |

## 8. Error Handling Strategy

### 8.1 Backend Errors
| Error Type | HTTP Status | Response |
|------------|-------------|----------|
| Not authenticated | 401 | {"detail": "Could not validate credentials"} |
| Wrong user_id | 403 | {"detail": "Not authorized to access this conversation"} |
| Invalid message | 400 | {"detail": "Message validation error"} |
| Conversation not found | 404 | {"detail": "Conversation not found"} |
| AI timeout | 504 | {"detail": "AI service timeout, please try again"} |
| AI error | 502 | {"detail": "AI service error"} |

### 8.2 Frontend Error Handling
- Display error messages in chat window
- Retry button for failed messages
- Loading states during AI processing
- Graceful degradation if chat unavailable

## 9. Environment Configuration

### 9.1 New Environment Variables
```
# Add to backend/.env
OPENAI_API_KEY=sk-...
```

### 9.2 Config.py Addition
```python
class Settings(BaseSettings):
    # ... existing settings ...
    OPENAI_API_KEY: str
```

## 10. Dependencies

### 10.1 Backend (add to pyproject.toml)
```toml
dependencies = [
    # ... existing ...
    "openai>=1.0.0",
]
```

### 10.2 Frontend (no new dependencies needed)
- Will use existing React + Tailwind + TypeScript stack
- No need for external chat libraries since we're implementing custom UI

## 11. Database Migration Strategy

### 11.1 Migration Steps
1. Update models/__init__.py with new exports
2. Run: `uv run alembic revision --autogenerate -m "add_conversations_and_messages_tables"`
3. Review generated migration
4. Apply: `uv run alembic upgrade head`

### 11.2 Expected Migration
```python
def upgrade():
    op.create_table('conversations',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.String(), nullable=False, index=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_table('messages',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('conversation_id', sa.Integer(), sa.ForeignKey('conversations.id'), index=True),
        sa.Column('user_id', sa.String(), nullable=False, index=True),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
```

## 12. Testing Strategy

### 12.1 Unit Tests
- Tool functions with mocked TaskService
- ChatService with mocked OpenAI client
- Conversation/Message model validation

### 12.2 Integration Tests
- Chat endpoint with test database
- Full flow: message → AI processing → tool execution → database → response

### 12.3 Frontend Tests
- ChatMessage rendering
- ChatInput submission
- ChatWindow state management

## 13. Risk Analysis

### 13.1 Technical Risks
| Risk | Impact | Mitigation |
|------|--------|------------|
| OpenAI API rate limits | Chat unavailable | Implement retry with backoff, add caching |
| AI response latency | Poor UX | Show loading state, set timeout, implement streaming |
| OpenAI API costs | High operational costs | Implement usage tracking, add cost controls |
| Breaking Phase 2 | System regression | Strict isolation, thorough testing |

### 13.2 Mitigation Strategies
- Implement circuit breaker for AI calls
- Add timeout handling with fallback responses
- Thorough testing before deployment
- Clear error boundaries in UI

## 14. Deployment Considerations

### 14.1 Environment Setup
- Add OPENAI_API_KEY to production environment
- Verify Neon DB can handle additional tables
- No additional services required

### 14.2 Rollback Plan
- Chat feature is additive (doesn't modify Phase 2)
- Can disable by removing router registration
- Database tables can remain (no impact on tasks)

## 15. Success Metrics

- [ ] Chat endpoint responds within 10 seconds
- [ ] All 5 tools execute correctly
- [ ] Conversation history loads correctly
- [ ] Phase 2 tests still pass
- [ ] Frontend builds without TypeScript errors
- [ ] Users can complete full task management via chat
- [ ] AI correctly interprets natural language commands