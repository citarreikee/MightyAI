from ollama import chat,Message,Client

messages = [
        Message(role='user',content='''You have access to the following tools:
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
You must always select one of the above tools and respond with only a JSON object matching the following schema:
{{
  "tool": <name of the selected tool>,
  "tool_input": <parameters for the selected tool, matching the tool's JSON schema>
}}
input: turn off the light.''')
]

client = Client(host='http://127.0.0.1:11434/')
# response = client.chat(model='mollysama/rwkv-6-world:14b', messages=messages,)
response = client.chat(model='deepseek-r1:32b', messages=messages)

print(response)

