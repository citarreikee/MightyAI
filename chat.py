from ollama import chat, Message

response = chat(model="deepseek-r1:32b", messages=[Message(role='user', content='介绍一下你自己')])


import os
print(os.getenv('OLLAMA_HOST'))
print(response['message']['content'], type(response))