# %%
import tomli
import tomli_w
from parser import xml
from link import LLMLinkBase


PROMPT_COMPILER = '''
<RULE>
All texts must be formatted in XML format. XML element ::= <tag attribute="value">content</tag>
Tags determine the meaning and function of the content. The content must not contradict the definition of the tag.
</RULE>

<TAG name="RULE">
This tag defines rules. The defined content is absolute.
</TAG>

<TAG name="TAG">
This tag defines a tag. The defined content is absolute.
Attributes:
    - name : A tag name.
</TAG>

<TAG name="THINK">
This tag is used to describe the thought process.
The thought process must be described in detail step-by-step.
Attributes:
    - label (optional) : A label summarizing the contents.
</TAG>

<TAG name="LIST">
This tag is used to describe a collection of the same XML elements.
Multiple identical tags are included within this tag.
Two or more types of tags must not exist within the LIST tag.
<EXAMPLE>
<LIST>
<ELEMENT>content1</ELEMENT>
<ELEMENT>content2</ELEMENT>
<ELEMENT>content3</ELEMENT>
</LIST>
</EXAMPLE>
</TAG>

<TAG name="EXAMPLE">
This tag describes an example.
The content described within this tag does not affect anything outside this tag.
For example, tags defined within the EXAMPLE tag are invalid outside the tag.
</TAG>

<TAG name="PROCESS">
This tag describes the information processing process.
The assistant must perform information processing according to the content of this tag.
</PROCESS>

<TAG name="INPUT_TAGS">
Describes the correspondence between input (arguments) and tags.
The correspondence is described as
argument1=TAG1,argument2=TAG2,...
separated by commas.
</TAG>

<TAG name="OUTPUT_TAGS">
Describes the correspondence between output (returns) and tags.
The correspondence is described as
return1=TAG1,return2=TAG2,...
separated by commas.
Notes:
    - For array-type returns (those in the form List[element]), the return should correspond to the element tag of the LIST tag, not the LIST tag itself.
</TAG>

<TAG name="SOURCE">
This tag describes the specifications of the information processing process.
The information processing process is described in the form of a python docstring.
The information processing process consists of input (arguments), output (returns), and processing content.
</TAG>

<RULE role="assistant">
The assistant executes the following process for the SOURCE.
<PROCESS>
1. The assistant carefully considers the content of the given SOURCE using the THINK tag. The assistant contemplates what steps are necessary to achieve the given process.
2. The assistant defines tags corresponding to the input (arguments) and output (returns) described in the SOURCE. The tag names are generally set to the same names as the arguments and returns described in the SOURCE, but different names can be used to avoid duplication.
3. If deemed effective, the assistant may define additional tags to assist in information processing.
4. The assistant uses INPUT_TAGS and OUTPUT_TAGS to map the defined tags to the arguments and returns in the SOURCE. Ensure accurate mapping.
5. The assistant describes the flow of information processing using the defined tags within the PROCESS tag.
</PROCESS>

Below is an example.
<EXAMPLE>
Suppose the following SOURCE is given to the assistant.
<SOURCE>
"""Split the text into words and count the number of words.

Args:
    text (str): Any text.

Returns:
    words (List[word]): Words contained in the input text.
    num_words (int): The number of words contained in the input text.

"""
</SOURCE>

In this case, the assistant converts the SOURCE into a combination of INPUT_TAGS, OUTPUT_TAGS, and PROCESS as follows.
<THINK label="Analysis of SOURCE">
The given SOURCE describes a process to split the input text into words and count the number of words.
First, a tag corresponding to the input text, text, needs to be defined.
Since the output words is a list of words, a word tag corresponding to a word should be defined and output within a LIST tag.
The granularity of "words" is not specified in the SOURCE. Therefore, here, words are defined as a collection of characters separated by spaces.
When counting words, to accurately determine the number,
</THINK>

<TAG name="TEXT">
This tag describes the text to be split into words.
</TAG>

<TAG name="WORD">
This tag describes a word.
Attributes:
    - count (optional) : Describes the order of the word.
</TAG>

<TAG name="NUM_WORDS">
This tag describes the number of words. Only numbers can be described within this tag.
</TAG>

<PROCESS>
1. Split the given string by spaces to form words.
2. Output the processing result as
<LIST>
<WORD count="1">word1</WORD>
<WORD count="2">word2</WORD>
...
</LIST>
3. Finally, output the number of words using the NUM_WORDS tag.
</PROCESS>

<INPUT_TAGS>
text=text
</INPUT_TAGS>

<OUTPUT_TAGS>
words=word,num_words=num_words
</OUTPUT_TAGS>

</EXAMPLE>
</RULE>

<SOURCE>
{source}
</SOURCE>
'''.strip()
OUTPUT_VARIABLES = ["TAG", "PROCESS", "INPUT_TAGS", "OUTPUT_TAGS"]


PROMPT_BASE = """
<RULE>
All texts must be formatted in XML format. XML element ::= <tag attribute="value">content</tag>
Tags determine the meaning and function of the content. The content must not contradict the definition of the tag.
</RULE>

<TAG name="RULE">
This tag defines rules. The defined content is absolute.
</TAG>

<TAG name="TAG">
This tag defines a tag. The defined content is absolute.
Attributes:
    - name : A tag name.
</TAG>

<TAG name="THINK">
This tag is used to describe the thought process.
The thought process must be described in detail step-by-step.
Attributes:
    - label (optional) : A label summarizing the contents.
</TAG>

<TAG name="LIST">
This tag is used to describe a collection of the same XML elements.
Multiple identical tags are included within this tag.
Two or more types of tags must not exist within the LIST tag.
<EXAMPLE>
<LIST>
<ELEMENT>content1</ELEMENT>
<ELEMENT>content2</ELEMENT>
<ELEMENT>content3</ELEMENT>
</LIST>
</EXAMPLE>
</TAG>

<TAG name="EXAMPLE">
This tag describes an example.
The content described within this tag does not affect anything outside this tag.
For example, tags defined within the EXAMPLE tag are invalid outside the tag.
</TAG>

<TAG name="PROCESS">
This tag describes the information processing process.
The assistant must perform information processing according to the content of this tag.
</PROCESS>

<RULE role="assistant">
The assistant must perform information processing according to the flow described in the PROCESS and output the necessary tags and their contents.
</RULE>
""".strip()


class PromptGenerator(LLMLinkBase):
    def __init__(self, llm):
        super().__init__(llm, PROMPT_COMPILER)

    def format(self, source):
        prompt = self.prompt_template.format(source=source)
        return prompt

    def parse(self, text):
        output = {var: [] for var in OUTPUT_VARIABLES}
        for var in OUTPUT_VARIABLES:
            for leaf in xml.findall(xml.parse(text), var):
                output[var].append(xml.deparse([leaf]).strip())
        return output


class LLMCompiler:
    def __init__(self, llm):
        self.prompt_generator = PromptGenerator(llm)

    def compile(self, source):
        ret = self.prompt_generator(source)

        assert len(ret["INPUT_TAGS"]) == 1
        assert len(ret["OUTPUT_TAGS"]) == 1

        input_tags = xml.parse(ret["INPUT_TAGS"][0])[1]["content"][0].strip().split(",")
        input_tags = dict(map(lambda x: x.split("="), input_tags))
        output_tags = (
            xml.parse(ret["OUTPUT_TAGS"][0])[1]["content"][0].strip().split(",")
        )
        output_tags = dict(map(lambda x: x.split("="), output_tags))

        prompt = PROMPT_BASE
        prompt += "\n\n" + "\n\n".join(ret["TAG"])
        prompt += "\n\n" + "\n\n".join(ret["PROCESS"])

        # for arg, tag in input_tags.items():
        #     prompt += f'\n\n<{tag}>'
        #     prompt += '\n{' + arg + '}'
        #     prompt += f'\n<\\{tag}>'

        params = {
            "source": source,
            "prompt_template": prompt,
            "input_tags": input_tags,
            "output_tags": output_tags,
        }

        compiled = tomli_w.dumps(params, multiline_strings=True)
        return compiled


class CompiledLLMLink(LLMLinkBase):
    def __init__(self, llm, compiled):
        params = tomli.loads(compiled)
        super().__init__(llm, params["prompt_template"], docstring=params["source"])
        self.input_tags = params["input_tags"]
        self.output_tags = params["output_tags"]

    def format(self, **kwargs):
        prompt = self.prompt_template

        for arg in kwargs:
            if arg not in self.input_tags:
                continue

            tag = self.input_tags[arg]
            values = kwargs[arg]
            if not isinstance(values, list):
                values = [values]

            prompt += "\n"
            if len(values) > 1:
                prompt += "\n<LIST>"
            for value in values:
                prompt += f"\n<{tag}>"
                prompt += f"\n{value}"
                prompt += f"\n</{tag}>"
            if len(values) > 1:
                prompt += "\n</LIST>"
        return prompt

    def parse(self, text):
        outputs = {var: [] for var in self.output_tags}
        for var in self.output_tags:
            tag = self.output_tags[var]
            for leaf in xml.findall(xml.parse(text), tag):
                outputs[var].append(xml.deparse(leaf["content"]).strip())
        return outputs
