import os
from dotenv import load_dotenv
from ollama import Client
from tools import calculator, text_length, remove_whitespace
from agent import run_agent
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

    max_iterations = 5  # 设置最大迭代次数，防止无限循环

    result = run_agent(
        user_input=user_input,
        messages=messages,
        client=client,
        model=model,
        tools=[calculator, text_length, remove_whitespace],
        max_iterations=max_iterations
    )
    print("AI助手的回复:", result)