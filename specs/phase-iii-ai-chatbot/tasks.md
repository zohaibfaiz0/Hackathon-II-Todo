# Phase III Full-Stack Web Application - Task Breakdown

## Overview
This document outlines all implementation tasks required to create an AI-powered chatbot interface for managing todos through natural language. Tasks are organized in dependency order to ensure smooth development progression.

## Layer 1: Database Models

### T-301: Create Conversation SQLModel
**Description**: Create the Conversation model following the same pattern as existing SQLModel models
**Files**: `backend/src/hackathon_todo_api/models/conversation.py`
**Dependencies**: None
**Acceptance Criteria**:
- [ ] Conversation model created with id, user_id, created_at, updated_at fields
- [ ] Proper indexing on user_id field
- [ ] Follows SQLModel patterns from task.py and user.py
- [ ] Model inherits from SQLModel with proper table configuration
**Test Cases**:
- [ ] Model can be instantiated with valid data
- [ ] SQLModel properly generates table schema

### T-302: Create Message SQLModel
**Description**: Create the Message model with foreign key to conversations
**Files**: `backend/src/hackathon_todo_api/models/message.py`
**Dependencies**: T-301
**Acceptance Criteria**:
- [ ] Message model created with id, conversation_id, user_id, role, content, created_at
- [ ] Proper foreign key relationship to conversations table
- [ ] Role field constrained to "user" or "assistant"
- [ ] Proper indexing on conversation_id and user_id fields
**Test Cases**:
- [ ] Model can be instantiated with valid data
- [ ] Foreign key constraint works properly

### T-303: Create and apply Alembic migration
**Description**: Generate and apply migration for conversations and messages tables
**Files**: Alembic migration files, database
**Dependencies**: T-301, T-302
**Acceptance Criteria**:
- [ ] Alembic migration generated for conversations and messages tables
- [ ] Migration applied successfully to Neon database
- [ ] Tables exist in database with correct schema
**Test Cases**:
- [ ] `uv run alembic upgrade head` applies migration without errors
- [ ] Tables exist in database after migration

## Layer 2: Schemas

### T-304: Create Chat Pydantic schemas
**Description**: Create Pydantic schemas for chat request/response validation
**Files**: `backend/src/hackathon_todo_api/schemas/chat.py`
**Dependencies**: None
**Acceptance Criteria**:
- [ ] ChatRequest schema with conversation_id (optional) and message (required, 1-2000 chars)
- [ ] ChatResponse schema with conversation_id, response, tool_calls
- [ ] ToolCallInfo schema with tool, arguments, result
- [ ] Proper validation applied to fields
**Test Cases**:
- [ ] Schemas validate correct data
- [ ] Schemas reject invalid data with appropriate errors

## Layer 3: Tools

### T-305: Create tools module structure
**Description**: Set up the tools module structure for OpenAI function calling
**Files**: `backend/src/hackathon_todo_api/tools/__init__.py`, `backend/src/hackathon_todo_api/tools/todo_tools.py`
**Dependencies**: T-304
**Acceptance Criteria**:
- [ ] `__init__.py` created in tools directory
- [ ] `todo_tools.py` created with tool schema definitions
- [ ] Helper function to get all tool schemas implemented
- [ ] Tool schemas follow OpenAI function calling format
**Test Cases**:
- [ ] `get_all_tools()` function returns all tool schemas
- [ ] All tool schemas have correct format for OpenAI

### T-306: Implement add_task tool
**Description**: Implement the add_task tool function that calls task_service.create_task()
**Files**: `backend/src/hackathon_todo_api/tools/todo_tools.py`
**Dependencies**: T-305
**Acceptance Criteria**:
- [ ] Function calls task_service.create_task() with correct parameters
- [ ] OpenAI function schema defined for add_task
- [ ] Return format: {task_id, status: "created", title}
- [ ] Proper error handling implemented
**Test Cases**:
- [ ] Tool function creates a task successfully
- [ ] Returns correct format when successful
- [ ] Returns error format when failed

### T-307: Implement list_tasks tool
**Description**: Implement the list_tasks tool function that calls task_service.get_tasks()
**Files**: `backend/src/hackathon_todo_api/tools/todo_tools.py`
**Dependencies**: T-305
**Acceptance Criteria**:
- [ ] Function calls task_service.get_tasks() with correct parameters
- [ ] Supports status filter: "all", "pending", "completed"
- [ ] Return format: array of task objects
- [ ] Proper error handling implemented
**Test Cases**:
- [ ] Tool function lists tasks correctly
- [ ] Status filter works properly
- [ ] Returns correct format when successful

### T-308: Implement complete_task tool
**Description**: Implement the complete_task tool function that calls task_service.toggle_task_completion()
**Files**: `backend/src/hackathon_todo_api/tools/todo_tools.py`
**Dependencies**: T-305
**Acceptance Criteria**:
- [ ] Function calls task_service.toggle_task_completion() with correct parameters
- [ ] OpenAI function schema defined for complete_task
- [ ] Return format: {task_id, status: "completed", title}
- [ ] Proper error handling implemented
**Test Cases**:
- [ ] Tool function completes task successfully
- [ ] Returns correct format when successful
- [ ] Returns error format when failed

### T-309: Implement delete_task tool
**Description**: Implement the delete_task tool function that calls task_service.delete_task()
**Files**: `backend/src/hackathon_todo_api/tools/todo_tools.py`
**Dependencies**: T-305
**Acceptance Criteria**:
- [ ] Function calls task_service.delete_task() with correct parameters
- [ ] OpenAI function schema defined for delete_task
- [ ] Return format: {task_id, status: "deleted", title}
- [ ] Proper error handling implemented
**Test Cases**:
- [ ] Tool function deletes task successfully
- [ ] Returns correct format when successful
- [ ] Returns error format when failed

### T-310: Implement update_task tool
**Description**: Implement the update_task tool function that calls task_service.update_task()
**Files**: `backend/src/hackathon_todo_api/tools/todo_tools.py`
**Dependencies**: T-305
**Acceptance Criteria**:
- [ ] Function calls task_service.update_task() with correct parameters
- [ ] Supports updating title and/or description
- [ ] OpenAI function schema defined for update_task
- [ ] Return format: {task_id, status: "updated", title}
- [ ] Proper error handling implemented
**Test Cases**:
- [ ] Tool function updates task successfully
- [ ] Can update title and description separately
- [ ] Returns correct format when successful

## Layer 4: Agent

### T-311: Create TodoAgent class
**Description**: Create the TodoAgent class to interact with OpenAI's API
**Files**: `backend/src/hackathon_todo_api/agents/__init__.py`, `backend/src/hackathon_todo_api/agents/todo_agent.py`
**Dependencies**: T-305
**Acceptance Criteria**:
- [ ] `__init__.py` created in agents directory
- [ ] `todo_agent.py` created with TodoAgent class
- [ ] Initializes OpenAI AsyncOpenAI client
- [ ] Method to process messages with tools
- [ ] Handles tool calls and executes them
- [ ] Returns final response
**Test Cases**:
- [ ] TodoAgent can be instantiated
- [ ] process_message method returns expected response
- [ ] Tool calls are properly handled

### T-312: Create agent system prompt
**Description**: Define the system prompt for the AI agent
**Files**: `backend/src/hackathon_todo_api/agents/todo_agent.py`
**Dependencies**: T-311
**Acceptance Criteria**:
- [ ] System prompt defined in todo_agent.py
- [ ] Instructions for todo assistant behavior included
- [ ] Guidance on tool usage included
- [ ] Response format guidelines included
**Test Cases**:
- [ ] System prompt can be accessed
- [ ] Content aligns with chatbot requirements

## Layer 5: Chat Service

### T-313: Create ChatService class
**Description**: Create the ChatService class to handle chat logic
**Files**: `backend/src/hackathon_todo_api/services/chat_service.py`
**Dependencies**: T-303, T-311, T-312
**Acceptance Criteria**:
- [ ] ChatService class created with all required methods
- [ ] create_conversation(user_id) -> Conversation implemented
- [ ] get_conversation(conversation_id, user_id) -> Optional[Conversation] implemented
- [ ] add_message(conversation_id, user_id, role, content) -> Message implemented
- [ ] get_messages(conversation_id, limit=20) -> List[Message] implemented
- [ ] process_chat(user_id, message, conversation_id?) -> ChatResponse implemented
- [ ] Follows existing service patterns (AsyncSessionLocal usage)
**Test Cases**:
- [ ] All methods execute successfully with valid data
- [ ] Database operations work correctly
- [ ] Conversation state is managed properly

## Layer 6: Chat Route

### T-314: Create chat route
**Description**: Create the chat route endpoint
**Files**: `backend/src/hackathon_todo_api/routes/chat.py`
**Dependencies**: T-304, T-313
**Acceptance Criteria**:
- [ ] POST /{user_id}/chat endpoint created
- [ ] Uses get_current_user dependency for authentication
- [ ] Validates user_id matches token
- [ ] Returns ChatResponse with proper schema
**Test Cases**:
- [ ] Endpoint returns 401 for unauthenticated requests
- [ ] Endpoint returns 403 for wrong user_id
- [ ] Endpoint returns 200 with valid request

### T-315: Register chat router in main.py
**Description**: Register the chat router in the main application
**Files**: `backend/src/hackathon_todo_api/main.py`
**Dependencies**: T-314
**Acceptance Criteria**:
- [ ] Import added for chat router
- [ ] Router registered with app.include_router()
- [ ] No existing functionality modified
**Test Cases**:
- [ ] Chat endpoint is accessible at /api/{user_id}/chat
- [ ] Other endpoints still work

## Layer 7: Model Exports

### T-316: Update models __init__.py
**Description**: Add exports for Conversation and Message models
**Files**: `backend/src/hackathon_todo_api/models/__init__.py`
**Dependencies**: T-301, T-302
**Acceptance Criteria**:
- [ ] Conversation and Message added to exports
- [ ] No existing exports modified
**Test Cases**:
- [ ] Conversation and Message can be imported from models package

## Layer 8: Configuration

### T-317: Add OpenAI configuration
**Description**: Add OpenAI API key configuration to the backend
**Files**: `backend/src/hackathon_todo_api/config.py`, `backend/.env.example`
**Dependencies**: None
**Acceptance Criteria**:
- [ ] OPENAI_API_KEY setting added to Settings class
- [ ] Placeholder added to .env.example
- [ ] No existing settings modified
**Test Cases**:
- [ ] Settings loads OPENAI_API_KEY from environment
- [ ] Proper validation occurs for required API key

## Layer 9: Frontend Types

### T-318: Create chat TypeScript types
**Description**: Create TypeScript types for chat functionality
**Files**: `frontend/src/types/chat.ts`
**Dependencies**: None
**Acceptance Criteria**:
- [ ] ChatMessage type with id, role, content, timestamp, toolCalls?
- [ ] ToolCall type with tool, arguments, result
- [ ] ChatResponse type with conversation_id, response, tool_calls
- [ ] Conversation type with id, created_at, updated_at
- [ ] All types exported
**Test Cases**:
- [ ] Types compile without errors
- [ ] Types match backend schemas where applicable

## Layer 10: Frontend API

### T-319: Create chat API client
**Description**: Create API client for chat functionality following existing patterns
**Files**: `frontend/src/lib/chat.ts`
**Dependencies**: T-318
**Acceptance Criteria**:
- [ ] sendChatMessage function with proper signature
- [ ] Follows pattern from existing api.ts
- [ ] Includes proper error handling
- [ ] Attaches JWT token from session
**Test Cases**:
- [ ] API calls include authorization header when authenticated
- [ ] Errors are properly caught and formatted
- [ ] Function returns expected response format

## Layer 11: Frontend Components

### T-320: Create ChatMessage component
**Description**: Create the ChatMessage component for displaying messages
**Files**: `frontend/src/components/chat/ChatMessage.tsx`
**Dependencies**: T-318
**Acceptance Criteria**:
- [ ] Component accepts message prop of ChatMessage type
- [ ] User messages displayed right-aligned with blue background
- [ ] Assistant messages displayed left-aligned with gray background
- [ ] Timestamp displayed
- [ ] Tool calls optionally shown (collapsible)
**Test Cases**:
- [ ] Component renders user messages correctly
- [ ] Component renders assistant messages correctly
- [ ] Timestamps display properly

### T-321: Create ChatInput component
**Description**: Create the ChatInput component for sending messages
**Files**: `frontend/src/components/chat/ChatInput.tsx`
**Dependencies**: None
**Acceptance Criteria**:
- [ ] Component accepts onSend, disabled?, placeholder? props
- [ ] Text input with send button
- [ ] Enter key submits message
- [ ] Input disabled during loading
- [ ] Input cleared after send
**Test Cases**:
- [ ] Component calls onSend with message when submitted
- [ ] Enter key triggers submission
- [ ] Component disables when loading

### T-322: Create ChatWindow component
**Description**: Create the main ChatWindow component
**Files**: `frontend/src/components/chat/ChatWindow.tsx`
**Dependencies**: T-318, T-319, T-320, T-321
**Acceptance Criteria**:
- [ ] Component accepts initialConversationId? prop
- [ ] Manages state: messages, conversationId, isLoading, error
- [ ] Scrolls to bottom on new messages
- [ ] Calls sendChatMessage on submit
- [ ] Handles errors gracefully
- [ ] Shows loading indicator
**Test Cases**:
- [ ] Component manages messages state correctly
- [ ] Messages appear in the chat window
- [ ] Loading state works properly

### T-323: Create chat components index
**Description**: Create index file to export chat components
**Files**: `frontend/src/components/chat/index.ts`
**Dependencies**: T-320, T-321, T-322
**Acceptance Criteria**:
- [ ] Exports ChatWindow, ChatMessage, ChatInput
- [ ] No errors when importing from index
**Test Cases**:
- [ ] Components can be imported from the index file

## Layer 12: Dashboard Integration

### T-324: Add chat to dashboard
**Description**: Integrate the chat component into the dashboard page
**Files**: `frontend/src/app/dashboard/page.tsx`
**Dependencies**: T-322, T-323
**Acceptance Criteria**:
- [ ] Add chat toggle button (floating action button or tab)
- [ ] Show ChatWindow when toggled
- [ ] Options: slide-in panel, modal, or side-by-side with tasks
- [ ] Does not break existing task management UI
- [ ] Only adds new code, doesn't restructure existing
**Test Cases**:
- [ ] Chat toggle button appears in dashboard
- [ ] Chat window opens when toggled
- [ ] Existing task management UI still works

## Layer 13: Backend Testing

### T-325: Create backend chat tests
**Description**: Create tests for the chat functionality
**Files**: `backend/tests/test_chat.py`
**Dependencies**: T-314
**Acceptance Criteria**:
- [ ] Test that chat endpoint requires authentication
- [ ] Test that user cannot access other user's conversations
- [ ] Test that new conversation created when conversation_id omitted
- [ ] Test that messages saved to database
- [ ] Test that tool execution works (with mocked OpenAI)
**Test Cases**:
- [ ] All tests pass
- [ ] Coverage includes critical functionality

## Layer 14: Frontend Testing

### T-326: Create frontend chat tests
**Description**: Create tests for frontend chat components
**Files**: `frontend/tests/chat.test.tsx`
**Dependencies**: T-320, T-321, T-322
**Acceptance Criteria**:
- [ ] Test that ChatMessage renders correctly for user/assistant
- [ ] Test that ChatInput calls onSend with message
- [ ] Test that ChatWindow manages state correctly
**Test Cases**:
- [ ] All tests pass
- [ ] Critical component behaviors covered

## Layer 15: Documentation

### T-327: Update documentation
**Description**: Update documentation with Phase 3 information
**Files**: `README.md`, `backend/CLAUDE.md`, `frontend/CLAUDE.md`
**Dependencies**: All previous tasks
**Acceptance Criteria**:
- [ ] README.md updated with Phase 3 section
- [ ] backend/CLAUDE.md updated with chat-related info
- [ ] frontend/CLAUDE.md updated with chat-related info
- [ ] Documents new environment variables
- [ ] Documents Chat API endpoint
- [ ] Explains how to use chat feature
**Test Cases**:
- [ ] Updated documentation is clear and accurate
- [ ] New setup instructions work for new developers