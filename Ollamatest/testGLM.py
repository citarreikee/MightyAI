import time
import json
from deviceHA.devices import lamp
from zhipuai import ZhipuAI

# lamp.set_light_brightness(100)

# API Key
client = ZhipuAI(api_key="66a5c90dc6e941c392c14acdd546ea09.f6EdQPJuoCVHwJGU")  

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

messages = []


def parse_function_call(model_response,messages):
    # 处理函数调用结果，根据模型返回参数，调用对应的函数。
    # 调用函数返回结果后构造tool message，再次调用模型，将函数结果输入模型
    # 模型会将函数调用结果以自然语言格式返回给用户。
    if model_response.choices[0].message.tool_calls:
        for tool_call in model_response.choices[0].message.tool_calls:
        
            args = tool_call.function.arguments
        
            function_result = {}
            if tool_call.function.name == "lamp.set_light_brightness":
                function_result = lamp.set_light_brightness(int(json.loads(args).get('brightness')))
            if tool_call.function.name == "lamp.set_light_color_temperature":
                function_result = lamp.set_light_color_temperature(int(json.loads(args).get('temperature')))
            if tool_call.function.name == "lamp.toggle":
                function_result = lamp.toggle()
        messages.append({
            "role": "tool",
            "content": f"{json.dumps(function_result)}",
            "tool_call_id":tool_call.id
        })
        response = client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=messages,
            tools=tools,
        )
        print(response.choices[0].message)
        messages.append(response.choices[0].message.model_dump())

messages.append({"role": "system", "content": "你是智能显示器灯控制管家，根据用户的需求和你的专业能力调用相关的控制函数控制灯的亮度、色温和开关。"})

messages.append({"role": "user", "content": "我现在在看书"})                
response = client.chat.completions.create(
    model="glm-4",
    messages=messages,
    tools=tools,
)

print(response.choices[0].message)
messages.append(response.choices[0].message.model_dump())

parse_function_call(response,messages)


# # 请求示例
# response = client.chat.completions.create(
#   model="glm-4v-flash",  # 填写需要调用的模型编码
#   messages=[
#        {"role": "system", "content": "你是一个乐于解答各种问题的助手，你的任务是为用户提供专业、准确、有见地的建议。"},
#         {"role": "user", "content": """帮我查一下2024年1月1日从北京南站到上海的火车票"""},
#   ],
#   tools=tools,
#   tool_choice="auto",
#   stream=True,
# )


# # 同步调用
# print(response.choices[0].message.content)

# #异步调用
# task_id = response.id
# task_status = ''
# get_cnt = 0

# while task_status != 'SUCCESS' and task_status != 'FAILED' and get_cnt <= 40:
#     result_response = client.chat.asyncCompletions.retrieve_completion_result(id=task_id)
#     print(result_response)
#     task_status = result_response.task_status

#     time.sleep(2)
#     get_cnt += 1

# # 流式调用
# for chunk in response:
#     print(chunk.choices[0].delta.content, end='', flush=True)