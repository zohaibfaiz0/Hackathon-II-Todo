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