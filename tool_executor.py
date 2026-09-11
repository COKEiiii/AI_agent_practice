from tools import calculator, text_length
from validator import validate_calculator_args, validate_text_length_args

TOOL_REGISTRY = {
    "calculator": {"function": calculator, "validator": validate_calculator_args},
    "text_length": {"function": text_length, "validator": validate_text_length_args}
}


def execute_tool(tool_call):
    tool_name = tool_call["function"]["name"]
    tool_args = tool_call["function"]["arguments"]
    tool_function = TOOL_REGISTRY.get(tool_name, {}).get("function")
    tool_validator = TOOL_REGISTRY.get(tool_name, {}).get("validator")
    validated_args = tool_validator(**tool_args)
    if tool_function is None:
        return f"Error: Tool '{tool_name}' not found."
    if tool_name == "calculator":
        try:
            result = tool_function(**validated_args)
            return str(result)
        except (ValueError, KeyError, TypeError) as e:
            return f"Error: {str(e)}"
    elif tool_name == "text_length":
        try:
            result = tool_function(**validated_args)
            return str(result)
        except (ValueError, KeyError, TypeError) as e:
            return f"Error: {str(e)}"