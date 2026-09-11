def validate_calculator_args(args):
    try:
        a = float(args.get("a"))
        b = float(args.get("b"))
        operation = args.get("operation")
        if operation not in ["+", "-", "*", "/"]:
            raise ValueError("Invalid operation. Must be one of: +, -, *, /.")
        return {"a": a, "b": b, "operation": operation}
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid calculator arguments: {e}")

def validate_text_length_args(args):
    text = args.get("text")
    if not isinstance(text, str):
        raise ValueError("Invalid text_length argument: 'text' must be a string.")
    return {"text": text}

def validate_remove_whitespace_args(args):
    text = args.get("text")
    if not isinstance(text, str):
        raise ValueError("Invalid remove_whitespace argument: 'text' must be a string.")
    return {"text": text}