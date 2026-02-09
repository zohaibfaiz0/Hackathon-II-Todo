from fastapi import APIRouter, Request
from typing import Any, Dict

router = APIRouter()

@router.post("/events/task-created")
async def handle_task_created(request: Request):
    """
    Handle task.created event from Dapr PubSub.
    Dapr sends the event payload in the body.
    """
    try:
        # Dapr sends CloudEvent format
        body = await request.json()
        print(f"📥 RECEIVED EVENT via Dapr: {body}")
        
        # Here you could add logic (e.g., analytics, notifications)
        
        return {"status": "SUCCESS"}
    except Exception as e:
        print(f"Error processing event: {e}")
        return {"status": "ERROR"}