# API Contract: Kubernetes Deployment Endpoints

## Backend API Endpoints (Internal)

### Health Check
- **Path**: `/health`
- **Method**: GET
- **Purpose**: Verify backend service is running
- **Response**: 200 OK with status information

### Task Management API
- **Base Path**: `/api/v1/tasks`
- **Methods**: GET, POST, PUT, DELETE
- **Purpose**: Manage todo tasks
- **Authentication**: JWT token required
- **Response Format**: JSON

### User Authentication API
- **Base Path**: `/auth`
- **Methods**: POST
- **Purpose**: Handle user authentication
- **Response Format**: JWT token

## Database Connection
- **Protocol**: PostgreSQL wire protocol
- **Port**: 5432
- **Connection String Format**: `postgresql://username:password@postgres-service:5432/database_name`
- **SSL**: Not required for internal cluster communication

## Frontend Configuration
- **API Base URL**: `http://backend-service:8000` (internal) or `http://localhost:8000` (external)
- **Environment Variable**: `NEXT_PUBLIC_API_URL`
- **Communication Protocol**: HTTP/HTTPS