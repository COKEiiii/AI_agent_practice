from tools import calculator

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
    if tool_name == "calculator":
        try:
            a, b, operation = validate_calculator_args(tool_args)
            result = calculator(a, b, operation)
            return str(result)
        except (ValueError, KeyError, TypeError) as e:
            return f"Error: {str(e)}"
    else:
        return f"Error: Tool '{tool_name}' not recognized."