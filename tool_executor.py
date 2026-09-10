from tools import calculator, text_length

TOOL_REGISTRY = {
    "calculator": calculator,
    "text_length": text_length
}

def validate_calculator_args(args):
    try:
        a = float(args.get("a"))
        b = float(args.get("b"))
        operation = args.get("operation")
        if operation not in ["+", "-", "*", "/"]:
            raise ValueError("Invalid operation. Must be one of: +, -, *, /.")
        return a, b, operation
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid calculator arguments: {e}")

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
        text = tool_args["text"]
        if not isinstance(text, str):
            return "Error: 'text' argument must be a string."
        result = tool_function(text)
        return str(result)