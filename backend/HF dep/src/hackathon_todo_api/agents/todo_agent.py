import json
from typing import List, Dict, Any, Optional
from openai import AsyncOpenAI


class TodoAgent:
    """Agent that processes chat messages and executes todo management tools."""

    def __init__(self, api_key: str):
        """Initialize the agent with OpenAI API key.

        Args:
            api_key: OpenAI API key
        """
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        self.model = "gemini-2.5-flash"

    def _get_system_prompt(self) -> str:
        """Return the system prompt for the todo assistant."""
        return """You are a helpful and friendly Todo Assistant.

### 🛑 CRITICAL RULE: TASK IDs
1. **NEVER GUESS IDs.** Database IDs are random numbers (e.g., 20, 45, 103), NOT sequential (1, 2, 3).
2. If the user says "delete it", "mark the milk task done", or "update task 1":
   - **YOU MUST CALL `list_tasks` FIRST** to see the real IDs.
   - Find the task the user is referring to in the list.
   - Use that **exact database ID** for the action tool.
   - If you cannot find the task, tell the user gracefully.

### Your Tools
- **add_task**: Create task
- **list_tasks**: See tasks (ALWAYS run this before modifying specific tasks if you don't know the exact ID)
- **complete_task**: Mark complete
- **delete_task**: Delete task
- **update_task**: Modify task

### Response Style
- **Concise & Clean:** "Deleted 'Buy Milk'.", "Added 'Gym'."
- **No Technical Jargon:** Do not show JSON or raw IDs unless asked.
- **Visuals:** Use ✅ for done, ⬜ for pending, 🗑️ for deleted.
"""

    async def process_message(
        self,
        user_id: str,
        messages: List[Dict[str, str]],
        tools: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Process a conversation and return the AI response.

        Args:
            user_id: The ID of the user (for tool execution)
            messages: Conversation history [{"role": "user/assistant", "content": "..."}]
            tools: List of tool schemas for function calling

        Returns:
            Dict with 'response' (str) and 'tool_calls' (list of executed tools)
        """
        from ..tools.todo_tools import execute_tool

        # Add system prompt to messages
        full_messages = [
            {"role": "system", "content": self._get_system_prompt()},
            *messages
        ]

        tool_calls_info = []

        try:
            # Initial API call
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=full_messages,
                tools=tools if tools else None,
                tool_choice="auto" if tools else None
            )

            assistant_message = response.choices[0].message

            # Check if the model wants to call tools
            while assistant_message.tool_calls:
                # Process each tool call
                tool_results = []

                for tool_call in assistant_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    # Execute the tool
                    result = await execute_tool(
                        tool_name=function_name,
                        user_id=user_id,
                        **function_args
                    )

                    # Record tool call info
                    tool_calls_info.append({
                        "tool": function_name,
                        "arguments": function_args,
                        "result": result
                    })

                    # Add tool result to messages
                    tool_results.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "content": json.dumps(result)
                    })

                # Add assistant message and tool results to conversation
                full_messages.append({
                    "role": "assistant",
                    "content": assistant_message.content or "",
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        }
                        for tc in assistant_message.tool_calls
                    ]
                })
                full_messages.extend(tool_results)

                # Get next response from model
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=full_messages,
                    tools=tools if tools else None,
                    tool_choice="auto" if tools else None
                )

                assistant_message = response.choices[0].message

            # Return final response
            return {
                "response": assistant_message.content or "I processed your request.",
                "tool_calls": tool_calls_info
            }

        except Exception as e:
            return {
                "response": f"I encountered an error: {str(e)}. Please try again.",
                "tool_calls": tool_calls_info
            }