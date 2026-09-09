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
    # 第一次调用LLM模型，获取模型的回复和工具调用信息
    response = client.chat(
        model=model,
        messages=messages,
        tools=[calculator]
    )

    tool_calls = response["message"]["tool_calls"]
    if tool_calls:
        messages.append(response["message"]) # 将模型的回复添加到消息列表中
        for tool_call in tool_calls:
            tool_name = tool_call["function"]["name"]
            tool_args = tool_call["function"]["arguments"]
            if tool_name == "calculator":
                print("Tool args:", tool_args)
                a = float(tool_args.get("a", 0)) # 如果没有提供参数a，则默认为0
                b = float(tool_args.get("b", 0))
                operation = tool_args.get("operation", "+")
                try:
                    result = calculator(a, b, operation)
                    print("Tool result:", result)
                except ValueError as e:
                    print("Error:", str(e))
            # 将工具的结果添加到消息列表中，以便在下一次调用LLM模型时使用
            messages.append(
                {
                    "role": "tool",
                    "content": str(result),
                    "tool_name": tool_name
                }
            )
        response = client.chat(
            model=model,
            messages=messages,
            tools=[calculator]
        )
    print(response["message"]["content"])