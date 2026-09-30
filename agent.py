import json
from collections.abc import Mapping, Sequence
from typing import Any

from tool_executor import execute_tool

_MISSING = object()


def _read_field(value: Any, field: str, default: Any = None) -> Any:
    """Read a field from mappings and SDK response objects."""
    if value is None:
        return default

    getter = getattr(value, "get", None)
    if callable(getter):
        try:
            return getter(field, default)
        except TypeError:
            # Some dict-like SDK objects only accept one argument for get().
            try:
                return getter(field)
            except (KeyError, TypeError):
                return default

    return getattr(value, field, default)

def run_agent(
    user_input,
    messages,
    client,
    model,
    tools,
    max_llm_calls=10, # 最大调用LLM模型的次数
    max_tool_calls=8,
    max_same_tool_repeats=3, # 同一个工具同一组参数连续重复
    max_consecutive_tool_errors=3, # 防止工具连续执行失败，即使参数不同
    think=None
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
    response_message = {}

    while True:
        if llm_call_count >= max_llm_calls:
            print("达到最大LLM调用次数，停止调用LLM模型。")
            stop_reason = "max_llm_calls_reached"
            break

        # 第一次调用模型时，messages中只有用户输入的消息。之后，每次调用模型时，messages中会包含用户输入、助手的回复以及工具调用的结果。
        chat_kwargs = {
            "model": model,
            "messages": messages,
            "tools": tools, # 可供LLM调用的工具列表，模型可以选择调用这些工具来完成任务
        }
        if think is not None:
            chat_kwargs["think"] = think
        response = client.chat(**chat_kwargs)
        llm_call_count += 1

        response_message = _read_field(response, "message", _MISSING)
        if response_message is _MISSING or response_message is None:
            print("LLM返回了无效的响应，停止调用LLM模型。")
            stop_reason = "invalid_llm_response"
            break

        content = _read_field(response_message, "content", _MISSING)
        raw_tool_calls = _read_field(response_message, "tool_calls", _MISSING)
        if content is _MISSING and raw_tool_calls is _MISSING:
            print("LLM返回了无效的响应，停止调用LLM模型。")
            stop_reason = "invalid_llm_response"
            break

        content = "" if content is _MISSING or content is None else content
        if raw_tool_calls is _MISSING or raw_tool_calls is None:
            tool_calls: Sequence[Any] = ()
        elif isinstance(raw_tool_calls, Sequence) and not isinstance(
            raw_tool_calls, (str, bytes)
        ):
            tool_calls = raw_tool_calls
        else:
            print("LLM返回了无效的工具调用列表，停止调用LLM模型。")
            stop_reason = "invalid_llm_response"
            break
        print("本轮 tool_calls 数量:", len(tool_calls))

        if not tool_calls:
            completed = True
            break
        if tool_call_count >= max_tool_calls:
            print("达到最大工具调用次数，停止调用工具。")
            stop_reason = "max_tool_calls_reached"
            break
        raw_tool_call = tool_calls[0]  # 只处理第一个工具调用
        tool_function = _read_field(raw_tool_call, "function", _MISSING)
        tool_name = _read_field(tool_function, "name", _MISSING)
        tool_args = _read_field(tool_function, "arguments", _MISSING)
        if (
            tool_function is _MISSING
            or not isinstance(tool_name, str)
            or not isinstance(tool_args, Mapping)
        ):
            print("LLM返回了无效的工具调用，停止调用LLM模型。")
            stop_reason = "invalid_llm_response"
            break

        tool_call = {
            "function": {
                "name": tool_name,
                "arguments": dict(tool_args),
            }
        }
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
        print("模型调用工具：", tool_name, "参数：", tool_args, "结果：", tool_result)
        tool_call_count += 1

        # assistant_message用于保留模型请求调用工具的消息，tool_result用于保留工具调用的结果消息。assistant_message和tool_result都会被添加到messages中，供下一轮模型调用使用。
        
        assistant_message = {
            "role": "assistant",
            "content": content,
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
        messages.append(
            {
                "role": "assistant",
                "content": content,
            }
        ) # 使用标准字典保存回复，避免把 SDK 自定义对象混入历史消息
        return {
            "status": "completed",
            "content": content,
            "stop_reason": stop_reason,
            "llm_call_count": llm_call_count,
            "tool_call_count": tool_call_count
        } # 返回模型的最终回复
    else:
        final_content = _read_field(response_message, "content", "") or ""
        return{
            "status": "stopped",
            "content": final_content,
            "stop_reason": stop_reason,
            "llm_call_count": llm_call_count,
            "tool_call_count": tool_call_count
        }
