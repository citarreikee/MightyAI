import inspect
import json
import asyncio
from typing import List, Dict, Any

from deviceHA.devices import lamp, speaker


from ollama import Client
from ollama import chat, Message

import wave
import pyaudio
import whisper

import re

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

                    # 特殊处理方向参数
                    if param.name == "direction":
                        if arg_value in ("0", "1"):
                            kwargs[param.name] = int(arg_value)  # 字符串转整数
                        else:
                            raise ValueError("方向参数必须是'0'或'1'的字符串")
                    else:
                        # 通用类型转换
                        if param.annotation != param.empty:
                            kwargs[param.name] = param.annotation(arg_value)
                        else:
                            kwargs[param.name] = arg_value

                    # expected_type = param.annotation
                    # if expected_type != param.empty:
                    #     kwargs[param.name] = expected_type(arg_value)
                    # else:
                    #     kwargs[param.name] = arg_value
        except (ValueError, TypeError) as e:
            return f"参数验证失败：{str(e)}"

        # # 在执行方法前进行类型转换
        # if param.annotation == int and isinstance(arg_value, str):
        #     try:
        #         kwargs[param.name] = int(arg_value)
        #     except ValueError:
        #         raise ValueError(f"参数 {param.name} 需要整数类型")

        # 执行异步方法
        try:
            result = await method(**kwargs)
            return f"执行成功：{result}"
        except Exception as e:
            return f"执行错误：{str(e)}"

async def record_audio(model: whisper.Whisper, seconds: int = 5) -> str:
    """异步录音并转换为文本"""
    loop = asyncio.get_event_loop()
    
    def sync_record():
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        
        print("\n录音中...（正在聆听）")
        frames = []
        for _ in range(0, int(RATE / CHUNK * seconds)):
            data = stream.read(CHUNK)
            frames.append(data)
        
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        with wave.open("temp.wav", "wb") as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
        return "temp.wav"

    try:
        # 异步执行录音
        audio_file = await loop.run_in_executor(None, sync_record)
        # 异步执行语音识别
        result = await loop.run_in_executor(None, model.transcribe, audio_file)
        return result["text"].strip()
    except Exception as e:
        print(f"语音识别错误: {str(e)}")
        return ""

def chat(conversation_history, tools):
    model = "qwq"  # Replace with your desired model
    client = Client(host='http://192.168.0.102:11434/')
    llm_response = client.chat(model=model, messages=conversation_history, tools=tools)

    return llm_response

async def main():
    
    
    print("Starting chat with Mighty AI. Type 'exit' to quit.")
    # 初始化语音模型
    print("正在加载语音识别模型...")
    whisper_model = whisper.load_model("small")
    print("模型加载完成\n")
    
    # 初始化对话历史
    conversation_history = [
        {"role": "system", "content": "你是智能显示器灯控制管家，根据用户的需求和你的专业能力调用相关的控制函数控制灯。"}
    ]
    
    function_caller = MengliFunctionCall(lamp)
    tools = function_caller.get_tools_spec()

    print("语音控制已就绪，请说指令（说'退出'结束）")
    
    while True:
        # 语音输入
        user_input = await record_audio(whisper_model, seconds=5)
        
        # 处理退出指令
        if not user_input:
            continue
        if "退出" in user_input.lower():
            break
            
        print(f"\n用户输入: {user_input}")
        
        # 添加到对话历史
        conversation_history.append({"role": "user", "content": user_input})
        
        # 获取LLM响应
        try:
            llm_response = chat(conversation_history, tools)
            content = llm_response['message']['content']
            cleaned_content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL).strip()
            print(f"助手响应: {cleaned_content}")
            # speaker.play_text(cleaned_content)

            conversation_history.append(llm_response['message'])
            
            # 处理函数调用
            for tool_call in llm_response['message'].get("tool_calls", []):
                result = await function_caller.parse_function_call(tool_call["function"])
                print(f"设备反馈: {result}")

                conversation_history.append({"role": "tool","content": str(result),"tool_call_id":tool_call})
            llm_response = chat(conversation_history, tools)
            

                      
            
        except Exception as e:
            print(f"处理错误: {str(e)}")
        

if __name__ == "__main__":
    asyncio.run(main())