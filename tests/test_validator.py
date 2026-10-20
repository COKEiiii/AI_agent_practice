from validator import (
    validate_calculator_args,
    validate_remove_whitespace_args,
    validate_text_length_args,
    validate_read_text_file_args
)
import pytest
from pathlib import Path

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

def test_validate_read_text_file_args_valid():
    args = {"file_path": "example.txt"}
    result = validate_read_text_file_args(args)

    actual_path = Path(result["file_path"])
    assert actual_path.is_absolute()

    project_root = Path(__file__).resolve().parent.parent
    expected_path = (project_root/"data"/"example.txt").resolve()
    assert actual_path == expected_path

def test_validate_read_text_file_args_path_traversal():
    args = {"file_path": "../.env"}
    
    with pytest.raises(ValueError, match="must be within"):
        validate_read_text_file_args(args)