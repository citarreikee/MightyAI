import numpy as np
from ollama import chat, embeddings, Message

class KnowledgeBase:
    def __init__(self, filepath, split_marker="###", max_chunk_length=2560):
        self.split_marker = split_marker
        self.max_chunk_length = max_chunk_length
        self.docs = self.split_content(filepath)
        # self.embeds = self.encode(self.docs)
    
    def split_content(self, filepath):
        """按标识符或分块分割文档，支持大文件流式读取"""
        chunks = []
        current_chunk = ""
        
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:  # 流式读取避免内存问题<button class="citation-flag" data-index="7">
                # 检查标识符分割
                if self.split_marker in line:
                    split_point = line.index(self.split_marker)
                    # 处理标识符前的内容
                    if current_chunk + line[:split_point]:
                        chunks.append(current_chunk + line[:split_point])
                    current_chunk = ""
                    # 标识符后的内容暂存
                    current_chunk += line[split_point + len(self.split_marker):]
                else:
                    current_chunk += line
                
                # 达到最大长度时强制分割（防止过长段落）
                while len(current_chunk) >= self.max_chunk_length:
                    split_idx = min(self.max_chunk_length, len(current_chunk) - 1)  # 修正初始值
                    # 向前寻找最近的空格或标点作为分割点（语义友好）
                    while split_idx > 0 and current_chunk[split_idx] not in [' ', '.', ',', ';']:
                        split_idx -= 1
                    if split_idx <= 0:
                        split_idx = len(current_chunk)  # 直接取整个块
                    chunks.append(current_chunk[:split_idx])
                    current_chunk = current_chunk[split_idx:].lstrip()
        
        # 处理剩余内容
        if current_chunk:
            chunks.append(current_chunk)
        return chunks

    def encode(self, texts):
        """使用更高效的模型并添加优化策略"""
        from transformers import AutoTokenizer, AutoModel
        import torch
        
        # 推荐模型：Sentence-BERT或CLIP（比nomic更优<button class="citation-flag" data-index="3"><button class="citation-flag" data-index="5">）
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModel.from_pretrained(model_name)
        
        embeddings = []
        with torch.no_grad():
            for i in range(0, len(texts), 16):  # 批量处理优化<button class="citation-flag" data-index="9">
                batch = texts[i:i+16]
                inputs = tokenizer(batch, padding=True, truncation=True, return_tensors="pt", max_length=512)
                outputs = model(**inputs)
                embeddings.extend(outputs.last_hidden_state[:, 0, :].numpy())  # [CLS]向量
        
        return np.array(embeddings)
    

if __name__ == "__main__":
    ap = KnowledgeBase('api.md')
    print(ap.docs[0])