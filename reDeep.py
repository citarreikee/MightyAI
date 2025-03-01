import requests

response = requests.post(
    'http://localhost:11434/api/generate',
    json={
        'model': 'deepseek-r1:32b',  # 模型名称
        'prompt': '为什么天空是蓝色的？',  # 输入提示
        'stream': False,     # 是否流式输出
        'options': {        # 关键参数在此处设置
            'max_tokens': 100,
            'temperature': 0.7,
            'top_p': 0.9
        }
    }
)

print(response.json())