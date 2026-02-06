import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from httpx import AsyncClient, ASGITransport
from datetime import datetime

from src.hackathon_todo_api.main import app
from src.hackathon_todo_api.models.conversation import Conversation
from src.hackathon_todo_api.models.message import Message
from src.hackathon_todo_api.schemas.chat import ChatResponse


class TestChatEndpoint:
    """Tests for the chat endpoint."""

    @pytest.fixture
    def mock_token_data(self):
        """Mock token data for authenticated user."""
        return "test-user-123"

    @pytest.fixture
    def auth_headers(self):
        """Authorization headers with mock token."""
        return {"Authorization": "Bearer mock-valid-token"}

    @pytest.mark.asyncio
    async def test_chat_requires_authentication(self):
        """Test that chat endpoint returns 401 without auth."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/api/test-user-123/chat",
                json={"message": "Hello"}
            )
            assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_chat_forbidden_for_wrong_user(self):
        """Test that user cannot access another user's chat."""
        with patch("src.hackathon_todo_api.auth.jwt.verify_token") as mock_verify:
            mock_verify.return_value = MagicMock(user_id="different-user")

            transport = ASGITransport(app=app)
            async with AsyncClient(transport=transport, base_url="http://test") as client:
                response = await client.post(
                    "/api/test-user-123/chat",
                    json={"message": "Hello"},
                    headers={"Authorization": "Bearer mock-token"}
                )
                assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_chat_message_validation(self):
        """Test that empty messages are rejected."""
        with patch("src.hackathon_todo_api.auth.jwt.verify_token") as mock_verify:
            mock_verify.return_value = MagicMock(user_id="test-user-123")

            transport = ASGITransport(app=app)
            async with AsyncClient(transport=transport, base_url="http://test") as client:
                response = await client.post(
                    "/api/test-user-123/chat",
                    json={"message": ""},
                    headers={"Authorization": "Bearer mock-token"}
                )
                assert response.status_code == 422  # Validation error


class TestChatService:
    """Tests for ChatService."""

    @pytest.mark.asyncio
    async def test_create_conversation(self):
        """Test conversation creation."""
        from src.hackathon_todo_api.services.chat_service import ChatService

        with patch("src.hackathon_todo_api.services.chat_service.AsyncSessionLocal") as mock_session:
            mock_session_instance = AsyncMock()
            mock_session.return_value.__aenter__.return_value = mock_session_instance

            # Mock the conversation object
            mock_conv = Conversation(
                id=1,
                user_id="test-user",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            mock_session_instance.refresh = AsyncMock(side_effect=lambda x: setattr(x, 'id', 1))

            service = ChatService()
            # Note: This will still try to use settings.OPENAI_API_KEY
            # In real tests, you'd need to mock the settings too


class TestChatTools:
    """Tests for MCP-style tools."""

    @pytest.mark.asyncio
    async def test_add_task_tool(self):
        """Test add_task tool creates a task."""
        from src.hackathon_todo_api.tools.todo_tools import add_task_tool

        with patch("src.hackathon_todo_api.tools.todo_tools.create_task") as mock_create:
            mock_task = MagicMock()
            mock_task.id = 1
            mock_task.title = "Test task"
            mock_create.return_value = mock_task

            result = await add_task_tool(
                user_id="test-user",
                title="Test task",
                description="Test description"
            )

            assert result["status"] == "created"
            assert result["task_id"] == 1
            assert result["title"] == "Test task"

    @pytest.mark.asyncio
    async def test_list_tasks_tool(self):
        """Test list_tasks tool returns tasks."""
        from src.hackathon_todo_api.tools.todo_tools import list_tasks_tool

        with patch("src.hackathon_todo_api.tools.todo_tools.get_tasks") as mock_get:
            mock_task = MagicMock()
            mock_task.id = 1
            mock_task.title = "Test task"
            mock_task.description = "Description"
            mock_task.completed = False
            mock_get.return_value = [mock_task]

            result = await list_tasks_tool(user_id="test-user", status="all")

            assert result["status"] == "success"
            assert len(result["tasks"]) == 1
            assert result["tasks"][0]["title"] == "Test task"

    @pytest.mark.asyncio
    async def test_list_tasks_tool_filter_pending(self):
        """Test list_tasks filters pending tasks."""
        from src.hackathon_todo_api.tools.todo_tools import list_tasks_tool

        with patch("src.hackathon_todo_api.tools.todo_tools.get_tasks") as mock_get:
            completed_task = MagicMock()
            completed_task.id = 1
            completed_task.title = "Done"
            completed_task.description = ""
            completed_task.completed = True

            pending_task = MagicMock()
            pending_task.id = 2
            pending_task.title = "Pending"
            pending_task.description = ""
            pending_task.completed = False

            mock_get.return_value = [completed_task, pending_task]

            result = await list_tasks_tool(user_id="test-user", status="pending")

            assert len(result["tasks"]) == 1
            assert result["tasks"][0]["title"] == "Pending"

    @pytest.mark.asyncio
    async def test_complete_task_tool(self):
        """Test complete_task tool toggles completion."""
        from src.hackathon_todo_api.tools.todo_tools import complete_task_tool

        with patch("src.hackathon_todo_api.tools.todo_tools.toggle_task_completion") as mock_toggle:
            mock_task = MagicMock()
            mock_task.id = 1
            mock_task.title = "Test task"
            mock_task.completed = True
            mock_toggle.return_value = mock_task

            result = await complete_task_tool(user_id="test-user", task_id=1)

            assert result["status"] == "completed"
            assert result["task_id"] == 1

    @pytest.mark.asyncio
    async def test_complete_task_tool_not_found(self):
        """Test complete_task returns not_found for missing task."""
        from src.hackathon_todo_api.tools.todo_tools import complete_task_tool

        with patch("src.hackathon_todo_api.tools.todo_tools.toggle_task_completion") as mock_toggle:
            mock_toggle.return_value = None

            result = await complete_task_tool(user_id="test-user", task_id=999)

            assert result["status"] == "not_found"

    @pytest.mark.asyncio
    async def test_delete_task_tool(self):
        """Test delete_task tool removes task."""
        from src.hackathon_todo_api.tools.todo_tools import delete_task_tool

        with patch("src.hackathon_todo_api.tools.todo_tools.get_task_by_id") as mock_get:
            with patch("src.hackathon_todo_api.tools.todo_tools.delete_task") as mock_delete:
                mock_task = MagicMock()
                mock_task.id = 1
                mock_task.title = "Test task"
                mock_get.return_value = mock_task
                mock_delete.return_value = True

                result = await delete_task_tool(user_id="test-user", task_id=1)

                assert result["status"] == "deleted"
                assert result["task_id"] == 1

    @pytest.mark.asyncio
    async def test_update_task_tool(self):
        """Test update_task tool modifies task."""
        from src.hackathon_todo_api.tools.todo_tools import update_task_tool

        with patch("src.hackathon_todo_api.tools.todo_tools.update_task") as mock_update:
            mock_task = MagicMock()
            mock_task.id = 1
            mock_task.title = "Updated title"
            mock_update.return_value = mock_task

            result = await update_task_tool(
                user_id="test-user",
                task_id=1,
                title="Updated title"
            )

            assert result["status"] == "updated"
            assert result["title"] == "Updated title"