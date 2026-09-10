import os
from dotenv import load_dotenv
from ollama import Client
from tools import calculator
from tool_executor import execute_tool

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
    max_iterations = 5  # 设置最大迭代次数，防止无限循环
    iteration_count = 0
    completed = False

    while True:
        if iteration_count >= max_iterations:
            print("达到最大迭代次数，停止调用LLM模型。")
            break

        response = client.chat(
            model=model,
            messages=messages,
            tools=[calculator]
        )
        iteration_count += 1

        response_message = response.get("message", {})
        tool_calls = response_message.get("tool_calls", [])

        if not tool_calls:
            completed = True
            break

        messages.append(response_message) # 将模型的回复添加到消息列表中，这里的response_message[content]应该是空的，但是包含了工具调用信息(模型这一轮决定调用了哪个工具,用什么参数调用)
        for tool_call in tool_calls:
            tool_name = tool_call["function"]["name"]
            tool_result = execute_tool(tool_call)
            print("Tool result:", tool_result)
            messages.append(
                {
                    "role": "tool",
                    "content": tool_result,
                    "tool_name": tool_name
                }
            )

    if completed:
        print(response["message"]["content"])
        messages.append(response["message"]) # 将模型的回复添加到消息列表中
    else:
        print("LLM模型未能完成任务，请检查工具调用和参数。")