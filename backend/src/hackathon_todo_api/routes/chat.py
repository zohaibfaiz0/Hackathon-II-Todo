from fastapi import APIRouter, Depends, HTTPException, status

from ..schemas.chat import ChatRequest, ChatResponse
from ..services.chat_service import chat_service
from ..auth.jwt import get_current_user

router = APIRouter()


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: str,
    request: ChatRequest,
    current_user_id: str = Depends(get_current_user)
) -> ChatResponse:
    """
    Process a chat message and return the AI response.

    This endpoint allows users to interact with their tasks using natural language.
    The AI assistant can add, list, complete, delete, and update tasks based on
    the user's message.

    Args:
        user_id: The ID of the user (from URL path)
        request: The chat request containing message and optional conversation_id
        current_user_id: The authenticated user's ID (from JWT token)

    Returns:
        ChatResponse with conversation_id, response text, and any tool calls made

    Raises:
        HTTPException 403: If user_id doesn't match the authenticated user
    """
    # Verify that the requesting user is the same as the user in the path
    if str(current_user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's chat"
        )

    # Process the chat message
    response = await chat_service.process_chat(
        user_id=user_id,
        message=request.message,
        conversation_id=request.conversation_id
    )

    return response