from agent import run_agent


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