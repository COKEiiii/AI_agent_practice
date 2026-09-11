from tool_executor import execute_tool

def run_agent(
    user_input,
    messages,
    client,
    model,
    tools,
    max_iterations=5
)-> str:
    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )
    iteration_count = 0
    completed = False
    while True:
        if iteration_count >= max_iterations:
            print("达到最大迭代次数，停止调用LLM模型。")
            break

        response = client.chat(
            model=model,
            messages=messages,
            tools=tools
        )
        iteration_count += 1

        response_message = response.get("message", {})
        tool_calls = response_message.get("tool_calls") or []
        print("本轮 tool_calls 数量:", len(tool_calls))

        if not tool_calls:
            completed = True
            break

        # messages.append(response_message) # 将模型的回复添加到消息列表中，这里的response_message[content]应该是空的，但是包含了工具调用信息(模型这一轮决定调用了哪个工具,用什么参数调用)
        # for tool_call in tool_calls:
        tool_call = tool_calls[0]  # 只处理第一个工具调用
        tool_name = tool_call["function"]["name"]
        tool_result = execute_tool(tool_call)
        print("模型调用工具：", tool_name, "参数：", tool_call["function"]["arguments"], "结果：", tool_result)
        assistant_message = {
            "role": "assistant",
            "content": tool_result,
            "tool_name": tool_name
        }
        messages.append(assistant_message)  # 将工具调用结果添加到消息列表中
        
    if completed:
        messages.append(response["message"]) # 将模型的回复添加到消息列表中
        return response["message"]["content"] # 返回模型的最终回复
    else:
        return("LLM模型未能完成任务，请检查工具调用和参数。")