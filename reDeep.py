import requests

# 发送 POST 请求
response = requests.post(
    'http://localhost:11434/api/generate',
    json={
        'model': 'deepseek-r1:32b',  # 模型名称
        'prompt': '为什么天空是蓝色的？',  # 输入提示
        'stream': False,     # 是否流式输出
        'options': {         # 关键参数在此处设置
            'max_tokens': 100,
            'temperature': 0.7,
            'top_p': 0.9
        }
    }
)

# 解析响应数据
data = response.json()

# 提取并打印 'response' 和 'context' 的长度
response_text = data.get('response', '')  # 获取 'response' 字段，默认为空字符串
context_length = len(data.get('context', []))  # 获取 'context' 列表的长度，默认为空列表

# 打印结果
print("Response:")
print(response_text)
print("\nLength of Context:")
print(context_length)
