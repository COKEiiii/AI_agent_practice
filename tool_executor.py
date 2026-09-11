from tools import calculator, text_length, remove_whitespace
from validator import validate_calculator_args, validate_text_length_args, validate_remove_whitespace_args

TOOL_REGISTRY = {
    "calculator": {"function": calculator, "validator": validate_calculator_args},
    "text_length": {"function": text_length, "validator": validate_text_length_args},
    "remove_whitespace": {"function": remove_whitespace, "validator": validate_remove_whitespace_args}
}


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