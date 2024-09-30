# %%
import os
from anthropic import Anthropic


class AnthropicLLM:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if "model" not in kwargs:
            self.kwargs["model"] = "claude-3-5-sonnet-20240620"
        if "max_tokens" not in kwargs:
            self.kwargs["max_tokens"] = 200
        if "stream" not in kwargs:
            self.kwargs["stream"] = False
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def __call__(self, input_text):
        messages = [{"role": "user", "content": input_text}]
        response = self.client.messages.create(messages=messages, **self.kwargs)
        output_text = response.content[0].text
        return output_text


if __name__ == "__main__":
    llm = AnthropicLLM()
    print(llm("Hello, world!"))
