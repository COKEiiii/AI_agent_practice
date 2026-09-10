import os
from dotenv import load_dotenv
from ollama import Client
from tools import calculator, text_length
from tool_executor import execute_tool
from agent import run_agent
load_dotenv()

model = os.getenv("LLM_MODEL")
ollama_host = os.getenv("OLLAMA_HOST")

if not model:# 如果model没有值
    raise ValueError("LLM_MODEL not found")

client = Client(host=ollama_host)# 创建一个 Ollama 客户端对象

messages = [
    {
        "role": "system",
        "content": "You are a helpful AI assistant. Please briefly reply to the user's question."
    }
]

run_agent("", messages, client, model, [calculator, text_length])