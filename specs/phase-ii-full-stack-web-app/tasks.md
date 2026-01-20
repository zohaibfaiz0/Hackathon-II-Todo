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