from tool_executor import execute_tool

def run_agent(
    user_input,
    messages,
    client,
    model,
    tools,
    max_llm_calls=10,
    max_tool_calls=8
)-> str:
    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )
    llm_call_count = 0
    tool_call_count = 0
    completed = False

    while True:
        if tool_call_count >= max_tool_calls:
            print("达到最大工具调用次数，停止调用工具。")
            break
        if llm_call_count >= max_llm_calls:
            print("达到最大LLM调用次数，停止调用LLM模型。")
            break

        response = client.chat(
            model=model,
            messages=messages,
            tools=tools
        )
        llm_call_count += 1

        response_message = response.get("message", {})
        tool_calls = response_message.get("tool_calls") or []
        print("本轮 tool_calls 数量:", len(tool_calls))

        if not tool_calls:
            completed = True
            break

        tool_call = tool_calls[0]  # 只处理第一个工具调用
        tool_name = tool_call["function"]["name"]
        tool_result = execute_tool(tool_call)
        print("模型调用工具：", tool_name, "参数：", tool_call["function"]["arguments"], "结果：", tool_result)
        tool_call_count += 1

        assistant_message = {
            "role": "assistant",
            "content": response_message.get("content") or "",
            "tool_calls": [tool_call]
        }
        messages.append(assistant_message)

        messages.append(
            {
                "role": "tool",
                "content": tool_result,
                "tool_name": tool_name
            }
        )

    if completed:
        messages.append(response["message"]) # 将模型的回复添加到消息列表中
        return response["message"]["content"] # 返回模型的最终回复
    else:
        return("LLM模型未能完成任务，请检查工具调用和参数。")