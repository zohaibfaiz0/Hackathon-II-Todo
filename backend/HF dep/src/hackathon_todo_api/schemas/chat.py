from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None
    message: str = Field(min_length=1, max_length=2000)


class ToolCallInfo(BaseModel):
    tool: str
    arguments: Dict[str, Any]
    result: Dict[str, Any]


class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: List[ToolCallInfo] = []