import ollama
ollama.delete('qwq:latest')
i = ollama.list()
print(i)
