import tempfile
from tools import read_text_file
import os

def test_file_read():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", encoding="utf-8", delete=False) as f:
        f.write("这是临时文件")
    try:
        assert read_text_file(f.name) == "这是临时文件"
    finally:
        os.remove(f.name)