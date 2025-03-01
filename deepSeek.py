from ollama import AsyncClient

async def chat():
    client = AsyncClient()
    model = "deepseek-r1:32b"  # Replace with your desired model
    print("Starting chat with DeepSeek-R1. Type 'exit' to quit.")
    
    # Initialize the conversation history
    conversation_history = []
    conversation_history.append({'role':'system','content':'你是一个乐于解答各种问题的助手，你的任务是为用户提供专业、准确、有见地的建议。'})
    
    # Load the model into memory
    await client.chat(model=model, messages=[])
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break

        # Add the user's message to the conversation history
        conversation_history.append({'role': 'user', 'content': user_input})

        # Send user message and receive the assistant's response
        print("Assistant:")
        async for part in await client.chat(model=model, messages=conversation_history, stream=True):
            if 'message' in part:
                print(f"{part['message']['content']}", end='', flush=True)
        print("\n")
        # Add the assistant's message to the conversation history
        if 'message' in part:
           conversation_history.append({'role': 'assistant', 'content': part['message']['content']})
    
    # Unload the model from memory
    await client.chat(model=model, messages=[], keep_alive=0)

# Run the chat function
import asyncio
asyncio.run(chat())
