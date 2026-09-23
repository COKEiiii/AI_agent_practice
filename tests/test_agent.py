from agent import run_agent
from tools import calculator


class FakeClient:
    def chat(self, model, messages, tools):
        return {
            "message": {
                "content": "Hello!",
                "tool_calls": []
            }
        }
def test_agent_without_tool_call():
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        }
    ]

    result = run_agent(
        user_input="Hello",
        messages=messages,
        client=FakeClient(),
        model="fake-model",
        tools=[]
    )

    assert result["status"] == "completed"
    assert result["content"] == "Hello!"
    assert result["llm_call_count"] == 1
    assert result["tool_call_count"] == 0

class FakeToolClient:
    def __init__(self):
        self.call_count = 0
        self.received_messages = []
    def chat(self, model, messages, tools):
        self.received_messages.append(list(messages))
        self.call_count += 1
        if self.call_count == 1:
            return { # 这里相当于模拟LLM第一次调用返回的结果，里面包含了一个工具调用的请求-->calculator(a=10, b=5, operation="*")
                "message": {
                    "content": "",
                    "tool_calls": [{
                        "function": {
                            "name": "calculator",
                            "arguments": {"a": "10", "b": "5", "operation": "*"}
                        }
                    }]
                }
            }
        else:
            return {
                "message": {
                    "content": "The result is 50.",
                    "tool_calls": []
                }
            }
def test_agent_with_tool_call():
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        }
    ]

    fake_tool_client = FakeToolClient()

    result = run_agent(
        user_input="Hello",
        messages=messages,
        client=fake_tool_client,
        model="fake-model",
        tools=[calculator]
    )
    first_call_messages = fake_tool_client.received_messages[0]
    second_call_messages = fake_tool_client.received_messages[1]
    assistant_message = second_call_messages[-2]
    tool_args = assistant_message["tool_calls"][0]["function"]["arguments"]
    
    assert result["status"] == "completed"
    assert result["content"] == "The result is 50."
    assert result["llm_call_count"] == 2
    assert result["tool_call_count"] == 1
    assert fake_tool_client.call_count == 2

    assert second_call_messages[-1]["role"] == "tool"
    assert second_call_messages[-1]["content"] == "50.0"
    assert second_call_messages[-1]["tool_name"] == "calculator"
    assert first_call_messages[-1]["role"] == "user"
    assert first_call_messages[-1]["content"] == "Hello"

    assert assistant_message["role"] == "assistant"
    assert assistant_message["content"] == ""
    assert assistant_message["tool_calls"][0]["function"]["name"] == "calculator"
    assert tool_args["a"] == "10"
    assert tool_args["b"] == "5"
    assert tool_args["operation"] == "*"