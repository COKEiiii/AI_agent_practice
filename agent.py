from tool_executor import execute_tool
import json

def run_agent(
    user_input,
    messages,
    client,
    model,
    tools,
    max_llm_calls=10,
    max_tool_calls=8,
    max_same_tool_repeats=3
)-> str:
    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )
    llm_call_count = 0
    tool_call_count = 0
    last_tool_signature = None
    same_tool_repeat_count = 0
    completed = False
    stop_reason = None
    max_consecutive_tool_errors = 1  # 设置最大连续工具调用错误次数
    consecutive_tool_errors = 0

    while True:
        if llm_call_count >= max_llm_calls:
            print("达到最大LLM调用次数，停止调用LLM模型。")
            stop_reason = "max_llm_calls_reached"
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
        if tool_call_count >= max_tool_calls:
            print("达到最大工具调用次数，停止调用工具。")
            stop_reason = "max_tool_calls_reached"
            break
        tool_call = tool_calls[0]  # 只处理第一个工具调用
        tool_name = tool_call["function"]["name"]
        tool_args = tool_call["function"]["arguments"]
        tool_signature = (tool_name, json.dumps(tool_args, sort_keys=True))
        if tool_signature == last_tool_signature:
            same_tool_repeat_count += 1
            if same_tool_repeat_count > max_same_tool_repeats:
                print(f"工具 {tool_name} 重复调用超过 {max_same_tool_repeats} 次，停止调用工具。")
                stop_reason = "max_same_tool_repeats_reached"
                break
        else:
            same_tool_repeat_count = 1
        last_tool_signature = tool_signature

        tool_result = execute_tool(tool_call)
        if tool_result.startswith("Error:"):
            consecutive_tool_errors += 1
        else:
            consecutive_tool_errors = 0
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
        if consecutive_tool_errors >= max_consecutive_tool_errors:
            print(f"连续工具调用错误次数达到 {max_consecutive_tool_errors}，停止调用工具。")
            stop_reason = "max_consecutive_tool_errors_reached"
            completed = False

    if completed:
        messages.append(response["message"]) # 将模型的回复添加到消息列表中
        return response["message"]["content"] # 返回模型的最终回复
    else:
        return(f"LLM模型停止原因：{stop_reason}")