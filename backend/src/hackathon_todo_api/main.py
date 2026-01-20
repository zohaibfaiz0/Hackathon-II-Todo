from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import tasks, health, auth
from .config import settings
from .database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    await init_db()
    yield
    # Shutdown: cleanup if needed

app = FastAPI(title="Hackathon Todo API", version="1.0.0", lifespan=lifespan)

# Parse the ALLOWED_ORIGINS string into a list
allowed_origins = [origin.strip() for origin in settings.ALLOWED_ORIGINS.split(",")]

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(tasks.router, prefix="/api", tags=["tasks"])  # The task routes now include the user_id in the path

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "hackathon_todo_api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )