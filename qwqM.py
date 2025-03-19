import inspect
import json
import asyncio
from typing import List, Dict, Any

from deviceHA.devices import lamp

from ollama import Client
from ollama import chat, Message

class MengliFunctionCall:
    def __init__(self, lamp_instance):
        self.lamp = lamp_instance
        self.available_functions = self._get_available_functions()

    def _get_available_functions(self) -> List[Dict]:
        """完整的OpenAPI规范工具描述"""
        return [
            # 亮度控制 ------------------------
            {
                "type": "function",
                "function": {
                    "name": "set_light_brightness_up",
                    "description": "单独调节顶灯亮度",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "brightness": {
                                "type": "integer",
                                "minimum": 0,
                                "maximum": 100,
                                "description": "亮度百分比（0-100）"
                            }
                        },
                        "required": ["brightness"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "set_light_brightness_middle",
                    "description": "单独调节主灯亮度",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "brightness": {
                                "type": "integer",
                                "minimum": 0,
                                "maximum": 100,
                                "description": "亮度百分比（0-100）"
                            }
                        },
                        "required": ["brightness"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "set_light_brightness_night",
                    "description": "单独调节夜灯亮度",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "brightness": {
                                "type": "integer",
                                "minimum": 0,
                                "maximum": 100,
                                "description": "亮度百分比（0-100）"
                            }
                        },
                        "required": ["brightness"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "set_light_brightness_up_middle",
                    "description": "同时调节顶灯和主灯亮度",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "up": {"type": "integer", "minimum": 0, "maximum": 100},
                            "middle": {"type": "integer", "minimum": 0, "maximum": 100}
                        },
                        "required": ["up", "middle"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "set_all_light_brightness",
                    "description": "同时调节所有灯光亮度",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "up": {"type": "integer", "minimum": 0, "maximum": 100},
                            "middle": {"type": "integer", "minimum": 0, "maximum": 100},
                            "night": {"type": "integer", "minimum": 0, "maximum": 100}
                        },
                        "required": ["up", "middle", "night"]
                    }
                }
            },

            # 色温控制 ------------------------
            {
                "type": "function",
                "function": {
                    "name": "set_light_color_temp_up",
                    "description": "单独调节顶灯色温",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "temp": {
                                "type": "integer",
                                "minimum": 2000,
                                "maximum": 6000,
                                "description": "色温值（2000-6000K）"
                            }
                        },
                        "required": ["temp"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "set_light_color_temp_middle",
                    "description": "单独调节主灯色温",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "temp": {
                                "type": "integer",
                                "minimum": 2000,
                                "maximum": 6000,
                                "description": "色温值（2000-6000K）"
                            }
                        },
                        "required": ["temp"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "set_all_light_color_temp",
                    "description": "同时设置所有灯光色温",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "up": {"type": "integer", "minimum": 2000, "maximum": 6000},
                            "middle": {"type": "integer", "minimum": 2000, "maximum": 6000},
                            "night": {"type": "integer", "minimum": 2000, "maximum": 6000}
                        },
                        "required": ["up", "middle", "night"]
                    }
                }
            },

            # 电机控制 ------------------------
            {
                "type": "function",
                "function": {
                    "name": "set_motor_angle",
                    "description": "控制电机旋转角度",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "direction": {
                                "type": "string",
                                "enum": ["0", "1"],
                                "description": "0=反向，1=正向（字符串类型）"
                            },
                            "angle": {
                                "type": "integer",
                                "minimum": 0,
                                "maximum": 70,
                                "description": "旋转角度（0-70度）"
                            }
                        },
                        "required": ["direction", "angle"]
                    }
                }
            },

            # 闹钟设置 ------------------------
            {
                "type": "function",
                "function": {
                    "name": "set_alarm",
                    "description": "设置倒计时闹钟",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "hours": {
                                "type": "integer",
                                "minimum": 0,
                                "maximum": 24,
                                "description": "小时数（0-24）"
                            },
                            "minutes": {
                                "type": "integer",
                                "minimum": 0,
                                "maximum": 59,
                                "description": "分钟数（0-59）"
                            }
                        },
                        "required": ["hours", "minutes"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "cancel_alarm",
                    "description": "取消当前设置的闹钟",
                    "parameters": {"type": "object", "properties": {}}
                }
            },

            # 模式切换 ------------------------
            {
                "type": "function",
                "function": {
                    "name": "set_normal_mode",
                    "description": "切换至正常照明模式",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "set_reading_mode",
                    "description": "切换至阅读模式（预设优化参数）",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "set_sleep_mode",
                    "description": "切换至睡眠模式（低亮度暖光）",
                    "parameters": {"type": "object", "properties": {}}
                }
            }
        ]

    def get_tools_spec(self) -> List[Dict]:
        """获取符合LLM Function Calling规范的tools描述"""
        return self.available_functions

    async def parse_function_call(self, function_call: Dict[str, Any]) -> str:
        """解析并执行函数调用"""
        function_name = function_call.get("name", "")
        function_args = function_call.get("arguments", {})

        # 参数预处理
        if isinstance(function_args, str):
            try:
                function_args = json.loads(function_args)
            except json.JSONDecodeError:
                return "参数解析失败：无效的JSON格式"

        # 获取实际方法对象
        method = getattr(self.lamp, function_name, None)
        if not method or not inspect.iscoroutinefunction(method):
            return f"未找到可执行方法：{function_name}"

        # 参数验证
        try:
            sig = inspect.signature(method)
            kwargs = {}
            for param in sig.parameters.values():
                if param.name in function_args:
                    # 类型强制转换
                    arg_value = function_args[param.name]
                    expected_type = param.annotation
                    if expected_type != param.empty:
                        kwargs[param.name] = expected_type(arg_value)
                    else:
                        kwargs[param.name] = arg_value
        except (ValueError, TypeError) as e:
            return f"参数验证失败：{str(e)}"

        # 执行异步方法
        try:
            result = await method(**kwargs)
            return f"执行成功：{result}"
        except Exception as e:
            return f"执行错误：{str(e)}"

# 使用示例
async def main():
    function_caller = MengliFunctionCall(lamp)

    # 大模型返回的示例（模拟LLM输出）
    llm_response = {
        "tool_calls": [{
            "function": {
                "name": "set_all_light_brightness",
                "arguments": '{"up": 0, "middle": 0, "night": 0}'
            }
        }]
    }

    for tool_call in llm_response.get("tool_calls", []):
        result = await function_caller.parse_function_call(tool_call["function"])
        print(result)

async def chat():
    client = Client(host='http://192.168.0.102:11434/')
    model = "qwq"  # Replace with your desired model
    print("Starting chat with Mighty AI. Type 'exit' to quit.")
    
    # Initialize the conversation history
    conversation_history = []
    conversation_history.append({"role": "system", "content": "你是智能显示器灯控制管家，根据用户的需求和你的专业能力调用相关的控制函数控制灯。"})
    
    function_caller = MengliFunctionCall(lamp)
    tools=function_caller.available_functions
    print(tools) 

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break

        # Add the user's message to the conversation history
        conversation_history.append({'role': 'user', 'content': user_input})

        # Send user message and receive the assistant's response
        print("Assistant:")
        llm_response = client.chat(model=model, messages=conversation_history, tools=tools)
        # print(response['message']['content'])
        print(llm_response)

        for tool_call in llm_response['message'].get("tool_calls", []):
            result = await function_caller.parse_function_call(tool_call["function"])
            print(result)
        # Add the assistant's message to the conversation history
        # conversation_history.append({'role': 'assistant', 'content': part['message']['content']})
        conversation_history.append(llm_response['message'])
        

if __name__ == "__main__":
    asyncio.run(chat())