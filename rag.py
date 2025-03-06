import numpy as np
from ollama import chat, embeddings, Message

class knowledgeBase:
    def __init__(self, filepath):
        with open(filepath,'r',encoding='utf-8') as f:
            content = f.read()
        
        self.docs = self.split_content(content)
        self.embeds = self.encode(self.docs)

    @staticmethod
    def split_content(content, max_length = 256):
        chunks = []
        for i in range(0, len(content), max_length):
            chunks.append(content[i:i+max_length])
        return chunks
    
    @staticmethod
    def encode(texts):
        embeds = []
        for text in texts:
            response = embeddings(model='nomic-embed-text',prompt=text)
            embeds.append(response['embedding'])
        return np.array(embeds)
    
    @staticmethod
    def cosine_similarity(vec1, vec2):

        # 将输入转换为 NumPy 数组
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)

        # 检查向量维度是否一致
        if vec1.shape != vec2.shape:
            raise ValueError("两个向量的维度必须相同！")

        # 计算点积
        dot_product = np.dot(vec1, vec2)

        # 计算向量的模
        norm_vec1 = np.linalg.norm(vec1)
        norm_vec2 = np.linalg.norm(vec2)

        # 避免除以零的情况
        if norm_vec1 == 0 or norm_vec2 == 0:
            raise ValueError("向量的模不能为零！")

        # 计算余弦相似度
        similarity = dot_product / (norm_vec1 * norm_vec2)
        return similarity
    
    def search(self, text):
        max_simlarity = 0
        max_simlarity_index = 0
        e = self.encode([text])[0]
        for idx, te in enumerate(self.embeds):
            similarity = self.cosine_similarity(e ,te)
            if similarity > max_simlarity:
                max_simlarity = similarity
                max_simlarity_index = idx
        return self.docs[max_simlarity_index]
    
    def find_most_similar_matrix(self, text):

        query_vector = self.encode([text])[0]
        # 归一化向量库和查询向量
        norm_library = self.embeds / np.linalg.norm(self.embeds, axis=1, keepdims=True)
        norm_query = query_vector / np.linalg.norm(query_vector)

        # 计算余弦相似度
        similarities = np.dot(norm_library, norm_query)

        # 找到最大相似度的索引
        most_similar_index = np.argmax(similarities)

        return self.docs[most_similar_index]
    

class RAG:
    def __init__(self, model, kb:knowledgeBase):
        self.model = model
        self.kb = kb
        self.prompt_template = """
        基于：%s
        回答：%s
        """

    def chat(self, text):
        context = self.kb.search(text)

        prompt = self.prompt_template % (context, text)
        response =  chat(self.model, [Message(role='system',content=prompt)])
        return response['message']

        
    
if __name__ == "__main__":
    # rag = RAG('deepseek-r1:32b',knowledgeBase(''))

    # while True:
    #     q = input('Human:')
    #     r = rag.chat(q)
    #     print('Assistant:',r['content'])


    ap = knowledgeBase('api.md')
    # t1 = ap.search('Generate Embeddings')
    # t2 = ap.find_most_similar_matrix('Generate Embeddings')

    # import timeit

    # # 测试 search 方法（运行 10 次取平均）
    # time_search = timeit.timeit(lambda: ap.search('Generate Embeddings'), number=10)
    # print(f"search 方法平均耗时: {time_search / 10:.4f} 秒")

    # # 测试 find_most_similar_matrix 方法（运行 10 次取平均）
    # time_matrix = timeit.timeit(lambda: ap.find_most_similar_matrix('Generate Embeddings'), number=10)
    # print(f"find_most_similar_matrix 方法平均耗时: {time_matrix / 10:.4f} 秒")
