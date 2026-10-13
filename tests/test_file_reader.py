import tempfile
from tools import read_text_file
import os
import pytest

def test_file_read():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", encoding="utf-8", delete=False) as f:
        f.write("这是临时文件")
    try:
        assert read_text_file(f.name) == "这是临时文件"
    finally:
        os.remove(f.name)

def test_file_read_empty():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", encoding="utf-8", delete=False) as f:
        pass
    try:
        with pytest.raises(ValueError, match="文件为空"): # 如果 read_text_file(f.name) 没有抛出 ValueError, 或者抛出的 ValueError 的信息不是 "文件为空"，那么测试就会失败
            read_text_file(f.name)
    finally:
        os.remove(f.name)