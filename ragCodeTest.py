import numpy as np
from ollama import chat, embeddings, Message, Client

client = Client(host='http://localhost:11434/')

class knowledgeBase:
    def __init__(self, filepath):
        with open(filepath,'r',encoding='utf-8') as f:
            self.content = f.read()

class RAG:
    def __init__(self, model, kb:knowledgeBase):
        self.model = model
        self.kb = kb
        self.prompt_template = """
        基于API文档：%s
        结合用户需求：%s
        生成代码缺少的部分：
        from config import HOME_ASSISTANT_TOKEN
        from yeelinkLamp22Cad9Light import YeelinkLamp22Cad9Light
        import datetime
        import time
        
        lamp = YeelinkLamp22Cad9Light(HOME_ASSISTANT_TOKEN)
        
        if __name__ == "__main__":
        "这里是你写代码的地方"
        
        """

    def chat(self, text):
        context = self.kb.content

        prompt = self.prompt_template % (context, text)
        response = client.chat(self.model, [Message(role='system',content=prompt)])
        return response['message']

if __name__ == "__main__":
    # ap = knowledgeBase('api.md')
    # print(ap.content)
    rag = RAG('deepseek-r1:32b',knowledgeBase('api.md'))

    while True:
        q = input('Human:')
        r = rag.chat(q)
        print('Assistant:',r['content'])