import os

from dotenv import load_dotenv
from ollama import Client
from tools import calculator

load_dotenv()

model = os.getenv("LLM_MODEL")
ollama_host = os.getenv("OLLAMA_HOST")

if not model:# 如果model没有值
    raise ValueError("LLM_MODEL not found")

def validate_calculator_args(args):
    try:
        a = float(args.get("a"))
        b = float(args.get("b"))
        operation = args.get("operation")
        if operation not in ["+", "-", "*", "/"]:
            raise ValueError("Invalid operation. Must be one of: +, -, *, /.")
        return a, b, operation
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid calculator arguments: {e}")

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

    response_message = response.get("message", {})
    tool_calls = response_message.get("tool_calls", [])

    if tool_calls:
        messages.append(response_message) # 将模型的回复添加到消息列表中，这里的response_message[content]应该是空的，但是包含了工具调用信息(模型这一轮决定调用了哪个工具,用什么参数调用)
        for tool_call in tool_calls:
            tool_name = tool_call["function"]["name"]
            tool_args = tool_call["function"]["arguments"]
            if tool_name == "calculator":
                print("Tool args:", tool_args)
                try:
                    a, b, operation = validate_calculator_args(tool_args)
                    result = calculator(a, b, operation)
                    tool_result = str(result)
                    print("Tool result:", result)
                except (ValueError, KeyError, TypeError) as e:
                    print("Error:", str(e))
                    tool_result = f"Error: {str(e)}"
            else:
                tool_result = f"Error: Tool '{tool_name}' not recognized."
                print(tool_result)
            # 将工具的结果添加到消息列表中，以便在下一次调用LLM模型时使用
            messages.append(
                {
                    "role": "tool",
                    "content": tool_result,
                    "tool_name": tool_name
                }
            )
        response = client.chat( # 第二次调用LLM模型，获取模型的最终回复
            model=model,
            messages=messages,
            tools=[calculator]
        )
    print(response["message"]["content"])
    messages.append(response["message"]) # 将模型的回复添加到消息列表中