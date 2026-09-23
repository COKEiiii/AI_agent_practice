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
    def chat(self, model, messages, tools):
        self.call_count += 1
        if self.call_count == 1:
            return {
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
        tools=[calculator]  # Assuming calculator_tool is defined elsewhere in your code
    )

    assert result["status"] == "completed"
    assert result["content"] == "The result is 50."
    assert result["llm_call_count"] == 2
    assert result["tool_call_count"] == 1
    assert fake_tool_client.call_count == 2