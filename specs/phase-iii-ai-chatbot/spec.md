# Phase III: AI-Powered Todo Chatbot Specification

## 1. Feature Overview

### 1.1 Description
Create an AI-powered chatbot interface for managing todos through natural language. Users can add, view, update, delete, and complete tasks by simply typing commands like "Add a task to buy groceries" or "What's pending?".

### 1.2 Goals
- Enable conversational task management through natural language
- Integrate OpenAI ChatKit for the frontend UI
- Leverage OpenAI Agents SDK with MCP for AI logic and tool execution
- Maintain seamless integration with existing task management system
- Preserve all existing Phase II functionality

### 1.3 Success Criteria
- Users can manage tasks via chat commands using natural language
- AI correctly interprets user intent and executes appropriate tools
- Conversation history persists across sessions
- All existing Phase II functionality remains intact
- System meets performance and scalability requirements

## 2. User Stories

### US-301: Send Chat Message
**As a** logged-in user
**I want to** send a natural language message to the chatbot
**So that** I can manage my tasks conversationally

**Acceptance Criteria:**
- Given I am authenticated
- When I POST to /api/{user_id}/chat with a message
- Then I receive an AI-generated response
- And conversation_id is returned (new or existing)
- And any tool_calls are included in response

**Error Cases:**
- 401 if not authenticated
- 403 if user_id doesn't match token
- 400 if message is empty or too long

### US-302: Add Task via Chat
**As a** logged-in user
**I want to** say "Add a task to buy groceries"
**So that** a task is created without using the form

**Acceptance Criteria:**
- Given I send a message with add/create/remember intent
- When the AI processes the message
- Then add_task tool is invoked
- And task is created in database
- And confirmation response is returned

**Natural Language Triggers:**
- "Add a task to..."
- "Create a task for..."
- "I need to remember to..."
- "Remind me to..."
- "New task:..."

### US-303: List Tasks via Chat
**As a** logged-in user
**I want to** ask "What are my tasks?"
**So that** I can see my task list conversationally

**Acceptance Criteria:**
- Given I send a message with list/show/view intent
- When the AI processes the message
- Then list_tasks tool is invoked with appropriate filter
- And tasks are returned in readable format

**Natural Language Triggers:**
- "Show me my tasks" → list_tasks(status="all")
- "What's pending?" → list_tasks(status="pending")
- "What have I completed?" → list_tasks(status="completed")
- "List all tasks" → list_tasks(status="all")

### US-304: Complete Task via Chat
**As a** logged-in user
**I want to** say "Mark task 3 as done"
**So that** I can complete tasks conversationally

**Acceptance Criteria:**
- Given I send a message with complete/done/finish intent
- When the AI processes the message
- Then complete_task tool is invoked with task_id
- And task status is updated in database
- And confirmation response is returned

**Natural Language Triggers:**
- "Mark task 3 as complete"
- "I finished task 5"
- "Task 2 is done"
- "Complete the groceries task" (requires lookup)

### US-305: Delete Task via Chat
**As a** logged-in user
**I want to** say "Delete task 2"
**So that** I can remove tasks conversationally

**Acceptance Criteria:**
- Given I send a message with delete/remove intent
- When the AI processes the message
- Then delete_task tool is invoked with task_id
- And task is removed from database
- And confirmation response is returned

**Natural Language Triggers:**
- "Delete task 2"
- "Remove task 5"
- "Cancel the meeting task"

### US-306: Update Task via Chat
**As a** logged-in user
**I want to** say "Change task 1 to 'Call mom tonight'"
**So that** I can update tasks conversationally

**Acceptance Criteria:**
- Given I send a message with update/change/rename intent
- When the AI processes the message
- Then update_task tool is invoked with new values
- And task is updated in database
- And confirmation response is returned

**Natural Language Triggers:**
- "Change task 1 to 'New title'"
- "Update task 3 description to..."
- "Rename task 2 to..."

### US-307: Persistent Conversation History
**As a** logged-in user
**I want to** my chat history to persist across sessions
**So that** I can see previous messages after page refresh

**Acceptance Criteria:**
- Given I have an existing conversation
- When I provide conversation_id in request
- Then previous messages are loaded
- And AI has context of past interactions
- And new messages are appended

### US-308: Start New Conversation
**As a** logged-in user
**I want to** start a fresh conversation
**So that** I can begin without previous context

**Acceptance Criteria:**
- Given I omit conversation_id from request
- When I send a message
- Then a new conversation is created
- And new conversation_id is returned

## 3. Technical Requirements

### 3.1 Architecture
```
┌─────────────────┐     ┌──────────────────────────────────────────────┐     ┌─────────────────┐
│                 │     │ FastAPI Server                               │     │                 │
│ ChatKit UI      │     │ ┌────────────────────────────────────────┐   │     │ Neon DB         │
│ (Frontend)      │────▶│ │ POST /api/{user_id}/chat               │   │     │ (PostgreSQL)    │
│                 │     │ └───────────────┬────────────────────────┘   │     │                 │
│                 │     │                 │                            │     │ - tasks         │
│                 │     │                 ▼                            │     │ - users         │
│                 │     │ ┌────────────────────────────────────────┐   │     │ - conversations │
│                 │◀────│ │ OpenAI Agents SDK (Agent + Runner)     │   │     │ - messages      │
│                 │     │ └───────────────┬────────────────────────┘   │     │                 │
│                 │     │                 │                            │     │                 │
│                 │     │                 ▼                            │     │                 │
│                 │     │ ┌────────────────────────────────────────┐   │────▶│                 │
│                 │     │ │ MCP Server (Task Management Tools)     │   │◀────│                 │
│                 │     │ └────────────────────────────────────────┘   │     │                 │
└─────────────────┘     └──────────────────────────────────────────────┘     └─────────────────┘
```

### 3.2 Technology Stack
- **Frontend UI**: OpenAI ChatKit
- **AI Logic**: OpenAI Agents SDK
- **Tool Protocol**: Official MCP SDK (Model Context Protocol)
- **Backend**: FastAPI
- **Database**: Existing Neon PostgreSQL (with new tables)
- **Authentication**: Existing JWT auth (reuse get_current_user)

### 3.3 Stateless Architecture Requirements
The server MUST be stateless:
- NO conversation state stored in memory
- ALL state persisted to database
- Each request cycle: Load history → Process → Save → Respond
- Server can restart without losing conversations
- Enables horizontal scaling

### 3.4 Frontend Requirements
- Integration with existing dashboard layout
- Use ChatKit for UI components
- Maintain responsive design with Tailwind
- Preserve existing authentication flow
- Type-safe TypeScript implementation

### 3.5 Backend Requirements
- RESTful API design with proper HTTP status codes
- JWT-based authentication middleware
- Input validation and sanitization
- Proper error handling and logging
- Async processing for AI operations

### 3.6 Security Requirements
- **Authentication**: Chat endpoint requires valid JWT token
- **Authorization**: User can only access their own conversations
- **User Isolation**: MCP tools receive user_id from authenticated context
- **Validation**: Verify URL user_id matches token user_id (same pattern as tasks.py)
- **Data Protection**: Secure transmission with HTTPS
- **Input Validation**: Server-side validation for all inputs

## 4. API Specification

### 4.1 Chat Endpoint
**POST /api/{user_id}/chat**

Request Body:
```json
{
  "conversation_id": 123,
  "message": "Add a task to buy groceries"
}
```
- conversation_id: Optional. If omitted, creates new conversation.
- message: Required. User's natural language input (1-2000 chars).

Response Body:
```json
{
  "conversation_id": 123,
  "response": "I've created a new task 'Buy groceries' for you!",
  "tool_calls": [
    {
      "tool": "add_task",
      "arguments": {"title": "Buy groceries"},
      "result": {"task_id": 5, "status": "created", "title": "Buy groceries"}
    }
  ]
}
```

## 5. MCP Tools Specification (5 Required Tools)

### Tool 1: add_task
| Attribute | Value |
|-----------|-------|
| Purpose | Create a new task |
| Parameters | user_id (str, required), title (str, required), description (str, optional) |
| Returns | {task_id: int, status: "created", title: str} |
| Calls | task_service.create_task() |

### Tool 2: list_tasks
| Attribute | Value |
|-----------|-------|
| Purpose | Retrieve user's tasks |
| Parameters | user_id (str, required), status (str, optional: "all"/"pending"/"completed") |
| Returns | Array of task objects [{id, title, completed, ...}] |
| Calls | task_service.get_tasks() |

### Tool 3: complete_task
| Attribute | Value |
|-----------|-------|
| Purpose | Mark a task as complete |
| Parameters | user_id (str, required), task_id (int, required) |
| Returns | {task_id: int, status: "completed", title: str} |
| Calls | task_service.toggle_task_completion() |

### Tool 4: delete_task
| Attribute | Value |
|-----------|-------|
| Purpose | Remove a task |
| Parameters | user_id (str, required), task_id (int, required) |
| Returns | {task_id: int, status: "deleted", title: str} |
| Calls | task_service.delete_task() |

### Tool 5: update_task
| Attribute | Value |
|-----------|-------|
| Purpose | Modify task title or description |
| Parameters | user_id (str, required), task_id (int, required), title (str, optional), description (str, optional) |
| Returns | {task_id: int, status: "updated", title: str} |
| Calls | task_service.update_task() |

## 6. Database Schema

### 6.1 Conversation Model
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | int | PK, auto-increment | Unique identifier |
| user_id | str | NOT NULL, indexed | Owner of conversation |
| created_at | datetime | NOT NULL, default now | Creation timestamp |
| updated_at | datetime | NOT NULL, default now | Last activity timestamp |

### 6.2 Message Model
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | int | PK, auto-increment | Unique identifier |
| conversation_id | int | FK→conversations.id, indexed | Parent conversation |
| user_id | str | NOT NULL, indexed | Owner of message |
| role | str | NOT NULL, enum("user","assistant") | Message sender role |
| content | str | NOT NULL | Message text |
| created_at | datetime | NOT NULL, default now | Creation timestamp |

## 7. Implementation Constraints

### 7.1 Integration Requirements (MUST Reuse from Phase 2)
- task_service.py functions (all CRUD operations)
- get_current_user auth dependency
- AsyncSessionLocal database session pattern
- Existing Task and User models
- Authentication and authorization patterns

### 7.2 Preservation Requirements (MUST NOT Modify)
- routes/tasks.py
- routes/auth.py
- services/task_service.py
- models/task.py
- models/user.py
- Frontend api.ts (only add new methods, don't change existing)

### 7.3 Performance Requirements
- **Response Time**: Chat response < 10 seconds (including AI processing)
- **Message Length**: Max 2000 characters per message
- **History Limit**: Load last 20 messages for context
- **Error Recovery**: Graceful handling of AI timeouts/errors
- **Scalability**: Stateless design supports horizontal scaling

## 8. Acceptance Tests

### 8.1 Chat Functionality Tests
- Verify chat endpoint requires authentication
- Verify user can only access their own conversations
- Verify conversation history persists correctly
- Verify new conversations can be started

### 8.2 Tool Execution Tests
- Verify add_task tool creates tasks in database
- Verify list_tasks tool returns correct task lists
- Verify complete_task tool updates task status
- Verify delete_task tool removes tasks from database
- Verify update_task tool modifies task details

### 8.3 Natural Language Processing Tests
- Verify AI correctly interprets various task creation phrases
- Verify AI correctly interprets various task listing phrases
- Verify AI correctly interprets various task completion phrases
- Verify AI correctly interprets various task deletion phrases
- Verify AI correctly interprets various task update phrases

### 8.4 Error Handling Tests
- Verify graceful handling of malformed messages
- Verify proper error responses for invalid requests
- Verify graceful handling of AI service timeouts
- Verify authentication failures are handled properly

### 8.5 Security Tests
- Verify unauthenticated access to chat endpoint fails
- Verify users cannot access other users' conversations
- Verify user_id validation works correctly
- Verify database isolation is maintained