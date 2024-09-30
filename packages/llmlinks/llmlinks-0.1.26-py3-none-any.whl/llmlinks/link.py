# %%
from .parser import xml
from llmlinks.llm.openai_model import OpenAILLM


class LLMLinkBase:
    """LLMLinkの基底クラス"""

    def __init__(self, llm, prompt_template, *args, docstring=None, **kwargs):
        self.llm = llm
        self.prompt_template = prompt_template
        if docstring is not None:
            self.__doc__ = docstring

    def format(self, *args, **kwargs):
        raise NotImplementedError

    def parse(self, text):
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        prompt = self.format(**kwargs)
        ret = self.llm(prompt)
        outputs = self.parse(ret)
        return outputs


class LLMLink(LLMLinkBase):
    # Todo: SimpleLLMLink などに改名する（互換性のため現状そのまま）
    def __init__(
        self, llm, prompt_template, input_variables, output_variables, docstring=None
    ):
        super().__init__(llm, prompt_template, docstring=docstring)
        self.input_variables = input_variables
        self.output_variables = output_variables

    def format(self, **kwargs):
        inputs = {var: "None" for var in self.input_variables}
        inputs.update(kwargs)
        prompt = self.prompt_template.format(**kwargs)
        return prompt

    def parse(self, text):
        outputs = {var: [] for var in self.output_variables}
        for var in self.output_variables:
            for leaf in xml.findall(xml.parse(text), var):
                outputs[var].append(xml.deparse(leaf["content"]).strip())
        return outputs


if __name__ == "__main__":
    prompt = """
    <instruction>
    Please tell me the country whose capital is surrounded by the <city> tag. Please enclose the output in the <output> tag.
    </instruction>
    <city>
    {city}
    </city>
"""

    llm = LLMLink(
        llm=OpenAILLM(model="gpt-4o-2024-08-06"),
        prompt_template=prompt,
        input_variables=["city"],
        output_variables=["output"],
    )
    data = {"city": "Tokyo"}
    print(llm(**data))
