def calculator(a: float, b: float, operation: str) -> float:
    """
    Perform arithmetic calculations on numeric values.
    Only use this tool when the user explicitly requests a mathematical calculation.
    Do not use this tool for general conversation, memory, names, or non-mathematical questions.

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

def text_length(text: str) -> int:
    """
    Calculate the length of a given text string.
    Only use this tool when the user explicitly requests to know the length of a text.
    Do not use this tool for general conversation, memory, names, or non-text-length-related questions.

    Args:
        text: The input text string.
    """
    return len(text)

def remove_whitespace(text: str) -> str:
    """
    Remove all whitespace characters from a given text string.
    Only use this tool when the user explicitly requests to remove whitespace from a text.
    Do not use this tool for general conversation, memory, names, or non-whitespace-related questions.

    Args:
        text: The input text string.
    """
    return ''.join(text.split())