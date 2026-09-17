from validator import (
    validate_calculator_args,
    validate_remove_whitespace_args,
    validate_text_length_args
)
import pytest

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

def test_validate_calculator_args_invalid_operation():
    with pytest.raises(ValueError): # 我预期下面这段代码必须抛出 ValueError
        validate_calculator_args(
            {
                "a": "10",
                "b": "5",
                "operation": "%"
            }
        )

def test_validate_calculator_args_invalid_a():
    with pytest.raises(ValueError):
        validate_calculator_args(
            {
                "a": "abc",
                "b": "5",
                "operation": "*"
            }
        )