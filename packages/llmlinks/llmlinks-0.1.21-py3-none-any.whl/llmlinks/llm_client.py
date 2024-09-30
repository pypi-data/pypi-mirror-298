# %%
from llm.openai_model import OpenAILLM
from llm.google_model import GoogleLLM
from llm.anthropic_model import AnthropicLLM


class LLMClient:
    """
    様々な大規模言語モデルと対話するためのクライアントを初期化
    """

    def __init__(self, llm_name):
        self.llm = self.initialize_llm(llm_name)

    def initialize_llm(self, llm_name):
        """
        提供されたモデル名に基づいて大規模言語モデルを初期化
        """
        model_map = {
            "gpt-4o-2024-08-06": OpenAILLM,
            "gpt-4o-2024-05-13": OpenAILLM,
            "gpt-4o-mini-2024-07-18": OpenAILLM,
            "gpt-4-turbo-2024-04-09": OpenAILLM,
            "gpt-4-0125-preview": OpenAILLM,
            "gemini-1.0-pro": GoogleLLM,
            "gemini-1.5-pro": GoogleLLM,
            "gemini-1.5-flash": GoogleLLM,
            "claude-3-5-sonnet-20240620": AnthropicLLM,
            "claude-3-opus-20240229": AnthropicLLM,
        }
        if llm_name in model_map:
            return model_map[llm_name](model=llm_name)
        else:
            raise ValueError(f"未知のLLM: {llm_name}")

    def __call__(self, input_text):
        """
        クライアントインスタンスが呼び出されたときに実行される機能を実装します。
        """
        return self.llm(input_text)


if __name__ == "__main__":
    llm_name = "gpt-4o-2024-08-06"
    llm = LLMClient(llm_name)
    print(llm("Hello, world!"))
