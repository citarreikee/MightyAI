import re

# 原始内容
content = '''<think>\n好的，用户发来“你好”，我需要回应问候。作为灯控制管家，应该友好回应，并说明自己的能力。不需要调用任何函数，因为用户只是打招呼。应该用自然的中文回复，欢迎用户并提示可以如何协助调整灯光。保持简洁亲切。\n</think>\n\n你好！我是你的智能显示器灯控制管
家，可以帮你调节亮度、色温或开关灯。有什么需要我为你调整的吗？'''

# 用正则删除 <think>...</think> 标签及内容（含换行）
cleaned_content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL).strip()

# 结果输出
print(cleaned_content)