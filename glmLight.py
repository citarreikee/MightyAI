from ollama import AsyncClient

# 函数调用
tools = [
    {
        "type": "function",
        "function": {
            "name": "lamp.set_light_brightness",
            "description": "设置显示器挂灯的亮度",
            "parameters": {
                "type": "object",
                "properties": {
                    "brightness": {
                        "type": "string",
                        "description": "亮度，范围: 1 ~ 100，步长: 1",
                    },
                },
                "required": ["brightness"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "lamp.set_light_color_temperature",
            "description": "设置显示器挂灯的色温",
            "parameters": {
                "type": "object",
                "properties": {
                    "temperature": {
                        "type": "string",
                        "description": "色温，范围: 2700 ~ 6500  步长: 1",
                    },
                },
                "required": ["temperature"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "lamp.toggle",
            "description": "开关灯",
            "parameters": {
                "type": "object",
                "properties": {
                    "toggle": {
                        "type": "string",
                        "description": "打开或者关闭",
                    },
                },
                "required": ["toggle"],
            },
           
        }
    }
]

async def chat():
    client = AsyncClient()
    model = "deepseek-r1:32b"  # Replace with your desired model
    print("Starting chat with Mighty AI. Type 'exit' to quit.")
    
    # Initialize the conversation history
    conversation_history = []
    conversation_history.append({'role':'system','content':'''
You have access to the following tools:
{tools = [
    {
        "type": "function",
        "function": {
            "name": "lamp.set_light_brightness",
            "description": "设置显示器挂灯的亮度",
            "parameters": {
                "type": "object",
                "properties": {
                    "brightness": {
                        "type": "string",
                        "description": "亮度，范围: 1 ~ 100，步长: 1",
                    },
                },
                "required": ["brightness"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "lamp.set_light_color_temperature",
            "description": "设置显示器挂灯的色温",
            "parameters": {
                "type": "object",
                "properties": {
                    "temperature": {
                        "type": "string",
                        "description": "色温，范围: 2700 ~ 6500  步长: 1",
                    },
                },
                "required": ["temperature"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "lamp.toggle",
            "description": "开关灯",
            "parameters": {
                "type": "object",
                "properties": {
                    "toggle": {
                        "type": "string",
                        "description": "打开或者关闭",
                    },
                },
                "required": ["toggle"],
            },
           
        }
    }
]}
You can select one of the above tools or just response user's content and respond with only a JSON object matching the following schema:
{{
  "tool": <name of the selected tool>,
  "tool_input": <parameters for the selected tool, matching the tool's JSON schema>,
  "message": <direct response users content>
}}
'''})
    
    # Load the model into memory
    await client.chat(model=model, messages=[])
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break

        # Add the user's message to the conversation history
        conversation_history.append({'role': 'user', 'content': user_input})

        # Send user message and receive the assistant's response
        print("Assistant:")
        async for part in await client.chat(model=model, messages=conversation_history, stream=True):
            if 'message' in part:
                print(f"{part['message']['content']}", end='', flush=True)
        print("\n")
        # Add the assistant's message to the conversation history
        if 'message' in part:
           conversation_history.append({'role': 'assistant', 'content': part['message']['content']})
    
    # Unload the model from memory
    await client.chat(model=model, messages=[], keep_alive=0)

# Run the chat function
import asyncio
asyncio.run(chat())