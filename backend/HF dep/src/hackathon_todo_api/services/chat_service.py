from typing import List, Optional
from datetime import datetime
from sqlmodel import select

from ..database import AsyncSessionLocal
from ..models.conversation import Conversation
from ..models.message import Message
from ..schemas.chat import ChatResponse, ToolCallInfo
from ..agents.todo_agent import TodoAgent
from ..tools.todo_tools import get_all_tools
from ..config import settings


class ChatService:
    """Service for managing chat conversations and AI interactions."""

    def __init__(self):
        """Initialize the chat service."""
        # Agent will be created when needed with API key from settings
        self._agent: Optional[TodoAgent] = None

    @property
    def agent(self) -> TodoAgent:
        """Lazy initialization of the agent."""
        if self._agent is None:
            self._agent = TodoAgent(api_key=settings.GEMINI_API_KEY)
        return self._agent

    async def create_conversation(self, user_id: str) -> Conversation:
        """Create a new conversation for the user.

        Args:
            user_id: The ID of the user

        Returns:
            The created Conversation
        """
        async with AsyncSessionLocal() as session:
            conversation = Conversation(
                user_id=user_id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(conversation)
            await session.commit()
            await session.refresh(conversation)
            return conversation

    async def get_conversation(
        self,
        conversation_id: int,
        user_id: str
    ) -> Optional[Conversation]:
        """Get a conversation by ID, ensuring it belongs to the user.

        Args:
            conversation_id: The ID of the conversation
            user_id: The ID of the user (for authorization)

        Returns:
            The Conversation if found and authorized, None otherwise
        """
        async with AsyncSessionLocal() as session:
            statement = select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            )
            result = await session.execute(statement)
            return result.scalar_one_or_none()

    async def add_message(
        self,
        conversation_id: int,
        user_id: str,
        role: str,
        content: str
    ) -> Message:
        """Add a message to a conversation.

        Args:
            conversation_id: The ID of the conversation
            user_id: The ID of the user
            role: The role ("user" or "assistant")
            content: The message content

        Returns:
            The created Message
        """
        async with AsyncSessionLocal() as session:
            message = Message(
                conversation_id=conversation_id,
                user_id=user_id,
                role=role,
                content=content,
                created_at=datetime.utcnow()
            )
            session.add(message)

            # Update conversation's updated_at timestamp
            statement = select(Conversation).where(
                Conversation.id == conversation_id
            )
            result = await session.execute(statement)
            conversation = result.scalar_one_or_none()
            if conversation:
                conversation.updated_at = datetime.utcnow()

            await session.commit()
            await session.refresh(message)
            return message

    async def get_messages(
        self,
        conversation_id: int,
        limit: int = 20
    ) -> List[Message]:
        """Get messages for a conversation.

        Args:
            conversation_id: The ID of the conversation
            limit: Maximum number of messages to return (default 20)

        Returns:
            List of Messages in chronological order
        """
        async with AsyncSessionLocal() as session:
            statement = (
                select(Message)
                .where(Message.conversation_id == conversation_id)
                .order_by(Message.created_at.desc())
                .limit(limit)
            )
            result = await session.execute(statement)
            messages = result.scalars().all()
            # Reverse to get chronological order
            return list(reversed(messages))

    async def process_chat(
        self,
        user_id: str,
        message: str,
        conversation_id: Optional[int] = None
    ) -> ChatResponse:
        """Process a chat message and return the AI response.

        This is the main entry point for chat interactions.

        Args:
            user_id: The ID of the user
            message: The user's message
            conversation_id: Optional existing conversation ID

        Returns:
            ChatResponse with conversation_id, response, and tool_calls
        """
        # Create or get conversation
        if conversation_id is None:
            conversation = await self.create_conversation(user_id)
            conversation_id = conversation.id
        else:
            conversation = await self.get_conversation(conversation_id, user_id)
            if conversation is None:
                # Conversation not found or doesn't belong to user
                # Create a new one instead of failing
                conversation = await self.create_conversation(user_id)
                conversation_id = conversation.id

        # Save the user's message
        await self.add_message(
            conversation_id=conversation_id,
            user_id=user_id,
            role="user",
            content=message
        )

        # Get conversation history
        history = await self.get_messages(conversation_id)

        # Convert to format expected by agent
        messages = [
            {"role": msg.role, "content": msg.content}
            for msg in history
        ]

        # Get available tools
        tools = get_all_tools()

        # Process with AI agent
        try:
            result = await self.agent.process_message(
                user_id=user_id,
                messages=messages,
                tools=tools
            )

            response_text = result.get("response", "I processed your request.")
            tool_calls = result.get("tool_calls", [])

        except Exception as e:
            response_text = f"I'm sorry, I encountered an error: {str(e)}"
            tool_calls = []

        # Save the assistant's response
        await self.add_message(
            conversation_id=conversation_id,
            user_id=user_id,
            role="assistant",
            content=response_text
        )

        # Convert tool calls to response format
        tool_call_infos = [
            ToolCallInfo(
                tool=tc["tool"],
                arguments=tc["arguments"],
                result=tc["result"]
            )
            for tc in tool_calls
        ]

        return ChatResponse(
            conversation_id=conversation_id,
            response=response_text,
            tool_calls=tool_call_infos
        )


# Create a singleton instance for use in routes
chat_service = ChatService()