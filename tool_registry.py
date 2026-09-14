from tools import calculator, text_length, remove_whitespace
from validator import (
    validate_calculator_args,
    validate_text_length_args,
    validate_remove_whitespace_args
)

TOOL_REGISTRY = {
    "calculator": {
        "function": calculator,
        "validator": validate_calculator_args
    },
    "text_length": {
        "function": text_length,
        "validator": validate_text_length_args
    },
    "remove_whitespace": {
        "function": remove_whitespace,
        "validator": validate_remove_whitespace_args
    }
}

def get_llm_tools():
    return [
        config["function"]
        for config in TOOL_REGISTRY.values()
    ]