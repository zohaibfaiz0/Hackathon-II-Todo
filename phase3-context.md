# Phase 3 Context Report

## 1. Constitution Summary
Key principles that apply to Phase 3:
- **Prime Directive**: "No Task = No Code" - all code must follow a referenced Task ID
- **Architecture**: Maintain layered architecture with strict separation of concerns (PRESENTATION → APPLICATION → DOMAIN → INFRASTRUCTURE)
- **Technology Stack**: Use approved technologies only (Next.js 16+, FastAPI, SQLModel, Neon PostgreSQL, custom JWT auth)
- **Security**: All API endpoints require authentication, enforce user data isolation
- **Quality**: Type safety everywhere, validation at domain layer, fail-fast approach
- **Phase Transition**: Domain layer remains portable across phases, extend Phase II, never rewrite

## 2. Backend Patterns to Follow

### Router Registration Pattern
From `main.py` - how to add new router:
```python
from .routes import health, tasks, auth  # Import new route modules

# Include routers
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(tasks.router, prefix="/api", tags=["tasks"])
```

### SQLModel Pattern
From `task.py` - exact pattern for new models:
```python
class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    user_id: str = Field(index=True)  # Changed from UUID to string to match auth system

class Task(TaskBase, table=True):
    __tablename__ = "tasks"  # Explicitly define table name
    id: Optional[int] = Field(default=None, primary_key=True)  # Changed from UUID to int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Service Pattern
From `task_service.py` - function signatures, async pattern, session usage:
```python
async def get_tasks(user_id: str) -> List[TaskRead]:
    async with AsyncSessionLocal() as session:
        statement = select(Task).where(Task.user_id == user_id)
        result = await session.execute(statement)
        tasks = result.scalars().all()
        # Convert to response objects and return
```

### Route Pattern
From `tasks.py` - auth dependency, response models, error handling:
```python
@router.get("/{user_id}/tasks", response_model=List[TaskRead])
async def read_tasks(
    user_id: str,
    current_user_id: str = Depends(get_current_user)
):
    # Verify that the requesting user is the same as the user in the path
    if str(current_user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's tasks"
        )
    tasks = await get_tasks(current_user_id)
    return tasks
```

### Auth Dependency
From `jwt.py` - how get_current_user works, what it returns:
```python
def verify_token(token: str) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except jwt.PyJWTError:
        raise credentials_exception
    return token_data

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    token_data = verify_token(token)
    return token_data.user_id  # Returns user_id as string
```

### Database Session Pattern
From `database.py` - how to get async session:
```python
async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session

# Used with dependency injection:
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)
```

## 3. Frontend Patterns to Follow

### API Client Pattern
From `api.ts` - how to add new API methods:
```javascript
const apiRequest = async <T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> => {
  const sessionData = getSessionData()
  if (!sessionData) {
    throw new Error('User not authenticated')
  }

  const { userId, token } = sessionData
  let path = endpoint
  if (endpoint.startsWith('/tasks')) {
    path = `/${userId}/tasks` + endpoint.substring(6)
  }

  const url = `${API_BASE_URL}/api${path}`

  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      ...options.headers,
    },
  })

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}))
    throw new Error(errorData.detail || errorData.message || `HTTP error! status: ${response.status}`)
  }
  return response.json()
}
```

### TypeScript Types Pattern
From `types/index.ts` - how types are defined:
```typescript
export interface Task {
  id: number
  user_id: string
  title: string
  description: string
  completed: boolean
  created_at: string
  updated_at: string
}

export interface TaskInput {
  title: string
  description?: string
  completed?: boolean
}
```

### Component Pattern
From existing components - structure, props, state:
- Use 'use client' directive for interactive components
- Server components for static content
- All API calls go through `lib/api.ts`
- Auth state via `useSession()` hook from `lib/auth.tsx`
- State management with useState, useEffect, etc.

### Page Pattern
From `dashboard/page.tsx` - layout, data fetching:
- Client components with 'use client' directive
- Use useSession() for auth state
- Data fetching with useEffect for initial load
- Error handling and loading states
- Responsive design with Tailwind

## 4. Existing Function Signatures to Reuse

### TaskService Functions
```python
async def get_tasks(user_id: str) -> List[TaskRead]
async def get_task_by_id(task_id: int, user_id: str) -> Optional[TaskRead]
async def create_task(task_data: TaskCreate, user_id: str) -> TaskRead
async def update_task(task_id: int, task_update: TaskUpdate, user_id: str) -> Optional[TaskRead]
async def delete_task(task_id: int, user_id: str) -> bool
async def toggle_task_completion(task_id: int, user_id: str) -> Optional[TaskRead]
```

### Auth Functions
```python
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security))
    # Returns user_id as string from JWT token
```

## 5. Current Dependencies
### Backend
- FastAPI 0.115+
- SQLModel 0.0.22+
- Neon PostgreSQL (via asyncpg)
- PyJWT for authentication
- Passlib with bcrypt for password hashing
- Pydantic for data validation

### Frontend
- Next.js 16.1.4+
- React 19.0.0+
- TypeScript 5.0.0+
- Tailwind CSS

## 6. Environment Variables
Backend:
- DATABASE_URL: Neon PostgreSQL connection string
- SECRET_KEY: JWT signing secret
- ALGORITHM: JWT algorithm (default: HS256)
- ACCESS_TOKEN_EXPIRE_MINUTES: Token expiry (default: 30)
- FRONTEND_URL: Frontend URL for CORS
- ALLOWED_ORIGINS: CORS allowed origins

Frontend:
- NEXT_PUBLIC_API_URL: Backend API URL (default: http://localhost:8000)

## 7. File Naming Conventions
- Snake case for Python files: `task_service.py`, `jwt.py`, `database.py`
- PascalCase for classes: `Task`, `TaskCreate`, `TaskRead`
- CamelCase for functions: `get_current_user`, `create_task`
- Kebab case for component files: `TaskList.tsx`, `TaskForm.tsx`

## 8. Import Path Patterns
- Backend: Relative imports from parent package: `from ..auth.jwt import get_current_user`
- Frontend: Absolute imports from src: `import { Task } from '@/types'`, `import { getTasks } from '@/lib/api'`
- Standard library imports first, then third-party, then local
- Imports grouped and ordered: `from __future__ import annotations` at the top