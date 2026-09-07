import os

from dotenv import load_dotenv
from ollama import Client

load_dotenv()

model = os.getenv("LLM_MODEL")
ollama_host = os.getenv("OLLAMA_HOST")

if not model:# 如果model没有值
    raise ValueError("LLM_MODEL not found")

client = Client(host=ollama_host)# 创建一个 Ollama 客户端对象

messages = [
    {
        "role": "system",
        "content": "You are a helpful AI assistant. Please briefly reply to the user's question."
    }
]

while True:
    user_input = input("请输入您的问题：")
    if user_input.lower().strip() in ["exit", "quit"]:
        break

    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    response = client.chat(
        model=model,
        messages=messages,
    )

    print(response["message"]["content"])

    messages.append(
        {
            "role": "assistant",
            "content": response["message"]["content"]
        }
    )