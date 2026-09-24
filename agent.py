from tool_executor import execute_tool
import json

def run_agent(
    user_input,
    messages,
    client,
    model,
    tools,
    max_llm_calls=10, # 最大调用LLM模型的次数
    max_tool_calls=8,
    max_same_tool_repeats=3, # 同一个工具同一组参数连续重复
    max_consecutive_tool_errors=3 # 防止工具连续执行失败，即使参数不同
)-> dict:
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
    consecutive_tool_errors = 0

    while True:
        if llm_call_count >= max_llm_calls:
            print("达到最大LLM调用次数，停止调用LLM模型。")
            stop_reason = "max_llm_calls_reached"
            break

        # 第一次调用模型时，messages中只有用户输入的消息。之后，每次调用模型时，messages中会包含用户输入、助手的回复以及工具调用的结果。
        response = client.chat(
            model=model,
            messages=messages,
            tools=tools # 可供LLM调用的工具列表，模型可以选择调用这些工具来完成任务
        )
        llm_call_count += 1

        response_message = response.get("message", {}) # 如果key "message" 不存在，则返回一个空字典，但是message可能是None，这时仍然会返回None
        tool_calls = response_message.get("tool_calls") or [] # 如果key "tool_calls" 不存在，则返回一个空列表，如果tool_calls是None，则返回一个空列表
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
        tool_signature = (tool_name, json.dumps(tool_args, sort_keys=True)) # 数据类型为元组
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

        # assistant_message用于保留模型请求调用工具的消息，tool_result用于保留工具调用的结果消息。assistant_message和tool_result都会被添加到messages中，供下一轮模型调用使用。
        
        assistant_message = {
            "role": "assistant",
            "content": response_message.get("content") or "", # 如果模型没有返回content，则使用空字符串,防止NoneType报错；这里的content是模型的回复内容，可能是None
            "tool_calls": [tool_call] # 这里保存的是本轮处理的第一个工具调用，并将其放进 assistant 的 tool_calls 字段里。
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
            print(
                f"连续工具调用错误次数达到 "
                f"{max_consecutive_tool_errors}，停止调用工具。"
            )
            stop_reason = "max_consecutive_tool_errors_reached"
            completed = False
            break

    if completed:
        messages.append(response["message"]) # 将模型的回复添加到消息列表中
        return {
            "status": "completed",
            "content": response["message"]["content"],
            "stop_reason": stop_reason,
            "llm_call_count": llm_call_count,
            "tool_call_count": tool_call_count
        } # 返回模型的最终回复
    else:
        return{
            "status": "stopped",
            "content": response_message.get("content") or "",
            "stop_reason": stop_reason,
            "llm_call_count": llm_call_count,
            "tool_call_count": tool_call_count
        }