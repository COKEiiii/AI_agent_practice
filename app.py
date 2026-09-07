import os

from dotenv import load_dotenv
from ollama import Client
from tools import calculator

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
        tools=[calculator]
    )

    tool_calls = response["message"]["tool_calls"]
    if tool_calls:
        for tool_call in tool_calls:
            tool_name = tool_call["function"]["name"]
            tool_args = tool_call["function"]["arguments"]
            if tool_name == "calculator":
                a = float(tool_args.get("a", 0))
                b = float(tool_args.get("b", 0))
                operation = tool_args.get("operation", "+")
                try:
                    result = calculator(a, b, operation)
                    print("Tool result:", result)
                except ValueError as e:
                    print("Error:", str(e))

    print(response["message"]["content"])

    messages.append(
        {
            "role": "assistant",
            "content": response["message"]["content"]
        }
    )