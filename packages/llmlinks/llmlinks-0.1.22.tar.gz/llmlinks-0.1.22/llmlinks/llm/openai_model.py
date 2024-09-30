# %%
import os
import openai


class OpenAILLM:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if 'model' not in kwargs:
            self.kwargs['model'] = 'gpt-4o-2024-08-06'
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def __call__(self, input_text, as_system=True):
        messages = [
            {
                'role': 'system' if as_system else 'user',
                'content': input_text
            }
        ]
        response = self.client.chat.completions.create(
            messages=messages,
            **self.kwargs)
        output_text = response.choices[0].message.content
        return output_text

if __name__ == "__main__":
    llm = OpenAILLM()
    print(llm("Hello, world!"))
