def calculator(a: float, b: float, operation: str) -> float:
    """
    Perform a basic arithmetic calculation.

    Args:
        a: The first number.
        b: The second number.
        operation: One of "+", "-", "*", "/".
    """
    if operation == '+':
        return a + b
    elif operation == '-':
        return a - b
    elif operation == '*':
        return a * b
    elif operation == '/':
        if b != 0:
            return a / b
        else:
            raise ValueError("Cannot divide by zero.")
    else:
        raise ValueError("Invalid operation. Please choose from '+', '-', '*', or '/'.")