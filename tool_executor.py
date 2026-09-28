from tool_registry import TOOL_REGISTRY


def execute_tool(tool_call):
    tool_name = tool_call["function"]["name"]
    tool_args = tool_call["function"]["arguments"]
    tool_function = TOOL_REGISTRY.get(tool_name, {}).get("function")
    tool_validator = TOOL_REGISTRY.get(tool_name, {}).get("validator")

    if tool_function is None or tool_validator is None:
        return f"Error: Tool '{tool_name}' not found."
    
    try:
        validated_args = tool_validator(tool_args) # 返回dict
        result = tool_function(**validated_args) # 将上面返回的dict展开作为关键字参数传入函数
        return str(result)

    except (ValueError, KeyError, TypeError) as e:
        return f"Error: {str(e)}" # 这里把异常信息转换为字符串并返回，是为了避免让异常直接冲出execute_tool函数，中断整个程序的执行。