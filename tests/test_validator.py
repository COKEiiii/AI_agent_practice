from validator import (
    validate_calculator_args,
    validate_remove_whitespace_args,
    validate_text_length_args
)


def test_validate_calculator_args_valid():
    result = validate_calculator_args(
        {
            "a": "10",
            "b": "5",
            "operation": "*"
        }
    )

    assert result == {
        "a": 10.0,
        "b": 5.0,
        "operation": "*"
    }

def test_validate_text_length_args_valid():
    result = validate_text_length_args(
        {
            "text": "Hello, world!"
        }
    )

    assert result == {
        "text": "Hello, world!"
    }

def test_validate_remove_whitespace_args_valid():
    result = validate_remove_whitespace_args(
        {
            "text": "   Hello, world!   "
        }
    )

    assert result == {
        "text": "   Hello, world!   "
    }
