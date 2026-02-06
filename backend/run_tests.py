import asyncio
import traceback
from openai import AsyncOpenAI
from src.hackathon_todo_api.config import settings
from src.hackathon_todo_api.agents.todo_agent import TodoAgent
from src.hackathon_todo_api.tools.todo_tools import get_all_tools
from src.hackathon_todo_api.services.chat_service import ChatService

# Using Gemini 2.5 Flash as the stable 2026 workhorse
CURRENT_MODEL = "gemini-2.5-flash"

async def test_1_direct_call(client):
    print("\n=== TEST 1: Direct Gemini API Call ===")
    try:
        response = await client.chat.completions.create(
            model=CURRENT_MODEL,
            messages=[{'role': 'user', 'content': 'Say hello in 3 words'}],
            max_tokens=20
        )
        print(f"PASS: {response.choices[0].message.content}")
    except Exception as e:
        print(f"FAIL: {e}")

async def test_2_tool_calling(client):
    print("\n=== TEST 2: Tool Calling ===")
    tools = [{
        'type': 'function',
        'function': {
            'name': 'add_task',
            'description': 'Add a task to the todo list',
            'parameters': {
                'type': 'object',
                'properties': {'title': {'type': 'string'}},
                'required': ['title']
            }
        }
    }]
    try:
        response = await client.chat.completions.create(
            model=CURRENT_MODEL,
            messages=[{'role': 'user', 'content': 'Add a task to buy milk'}],
            tools=tools,
            tool_choice='auto'
        )
        msg = response.choices[0].message
        if msg.tool_calls:
            print(f"PASS: Tool called - {msg.tool_calls[0].function.name}")
            print(f"      Args: {msg.tool_calls[0].function.arguments}")
        else:
            print(f"WARN: No tool call, response: {msg.content}")
    except Exception as e:
        print(f"FAIL: {e}")

async def test_3_full_agent():
    print("\n=== TEST 3: Full TodoAgent ===")
    try:
        # Note: Ensure TodoAgent class uses CURRENT_MODEL internally or passes it here
        agent = TodoAgent(api_key=settings.GEMINI_API_KEY)
        result = await agent.process_message(
            user_id='test-user',
            messages=[{'role': 'user', 'content': 'What can you help me with?'}],
            tools=get_all_tools()
        )
        print(f"PASS: Agent responded")
        print(f"      Response preview: {result['response'][:70]}...")
        print(f"      Tool calls found: {len(result['tool_calls'])}")
    except Exception as e:
        print(f"FAIL: {e}")
        traceback.print_exc()

async def test_4_chat_service():
    print("\n=== TEST 4: Full ChatService ===")
    try:
        service = ChatService()
        result = await service.process_chat(
            user_id='live-test-user',
            message='Hello, what can you do?',
            conversation_id=None
        )
        print(f"PASS: ChatService works")
        print(f"      Conversation ID: {result.conversation_id}")
        print(f"      Response preview: {result.response[:70]}...")
    except Exception as e:
        print(f"FAIL: {e}")
        traceback.print_exc()

async def main():
    # Initialize the client once
    client = AsyncOpenAI(
        api_key=settings.GEMINI_API_KEY,
        base_url='https://generativelanguage.googleapis.com/v1beta/openai/'
    )

    await test_1_direct_call(client)
    await test_2_tool_calling(client)
    await test_3_full_agent()
    await test_4_chat_service()

    print("\n==============================================")
    print("All tests completed.")
    print("==============================================")

if __name__ == "__main__":
    asyncio.run(main())