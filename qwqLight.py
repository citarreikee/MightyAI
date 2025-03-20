from ollama import Client
from ollama import chat, Message

import time
import json
from deviceHA.devices import lamp

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
                        "type": "int",
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
                        "type": "int",
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
                        "type": "NONE",
                        "description": "每次调用触发开/关",
                    },
                },
                "required": ["toggle"],
            },
           
        }
    }
]

def parse_function_call(model_response,messages):
    client = Client(host='http://localhost:11434/')
    # 处理函数调用结果，根据模型返回参数，调用对应的函数。
    # 调用函数返回结果后构造tool message，再次调用模型，将函数结果输入模型
    # 模型会将函数调用结果以自然语言格式返回给用户。
    if model_response.message.tool_calls:
        for tool_call in model_response.message.tool_calls:
        
            args = tool_call.function.arguments
        
            function_result = {}
            if tool_call.function.name == "lamp.set_light_brightness":
                # function_result = lamp.set_light_brightness(int(json.loads(args).get('brightness')))
                function_result = lamp.set_light_brightness(int(args['brightness']))
            if tool_call.function.name == "lamp.set_light_color_temperature":
                function_result = lamp.set_light_color_temperature(int(args['temperature']))
            if tool_call.function.name == "lamp.toggle":
                function_result = lamp.toggle()
            messages.append({
                "role": "tool",
                "content": str(function_result),
                "tool_call_id":tool_call
            })
        response = client.chat(
            model="qwq",  
            messages=messages,
            tools=tools,
        )
        print(response['message']['content'])
        messages.append(response.message)

async def chat():
    client = Client(host='http://localhost:11434/')
    model = "qwq"  # Replace with your desired model
    print("Starting chat with Mighty AI. Type 'exit' to quit.")
    
    # Initialize the conversation history
    conversation_history = []
    conversation_history.append({"role": "system", "content": "你是智能显示器灯控制管家，根据用户的需求和你的专业能力调用相关的控制函数控制灯的亮度、色温和开关。"})
    

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break

        # Add the user's message to the conversation history
        conversation_history.append({'role': 'user', 'content': user_input})

        # Send user message and receive the assistant's response
        print("Assistant:")
        response = client.chat(model=model, messages=conversation_history, tools=tools)
        # print(response['message']['content'])
        print(response['message']['content'])
        # Add the assistant's message to the conversation history
        # conversation_history.append({'role': 'assistant', 'content': part['message']['content']})
        conversation_history.append(response['message'])
        parse_function_call(response,conversation_history)
    


if __name__ == "__main__":

    # Run the chat function
    import asyncio
    asyncio.run(chat())