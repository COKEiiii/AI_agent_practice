from tool_registry import TOOL_REGISTRY


def execute_tool(tool_call):
    tool_name = tool_call["function"]["name"]
    tool_args = tool_call["function"]["arguments"]
    tool_function = TOOL_REGISTRY.get(tool_name, {}).get("function")
    tool_validator = TOOL_REGISTRY.get(tool_name, {}).get("validator")

    if tool_function is None or tool_validator is None:
        return f"Error: Tool '{tool_name}' not found."
    
    try:
        validated_args = tool_validator(tool_args)
        result = tool_function(**validated_args)
        return str(result)

    except (ValueError, KeyError, TypeError) as e:
        return f"Error: {str(e)}"