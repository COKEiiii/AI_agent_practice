from tools import calculator, text_length
from validator import validate_calculator_args, validate_text_length_args

TOOL_REGISTRY = {
    "calculator": calculator,
    "text_length": text_length
}


def execute_tool(tool_call):
    tool_name = tool_call["function"]["name"]
    tool_args = tool_call["function"]["arguments"]
    tool_function = TOOL_REGISTRY.get(tool_name)
    if tool_function is None:
        return f"Error: Tool '{tool_name}' not found."
    if tool_name == "calculator":
        try:
            a, b, operation = validate_calculator_args(tool_args)
            result = tool_function(a, b, operation)
            return str(result)
        except (ValueError, KeyError, TypeError) as e:
            return f"Error: {str(e)}"
    elif tool_name == "text_length":
        try:
            text = validate_text_length_args(tool_args)
            result = tool_function(text)
            return str(result)
        except (ValueError, KeyError, TypeError) as e:
            return f"Error: {str(e)}"