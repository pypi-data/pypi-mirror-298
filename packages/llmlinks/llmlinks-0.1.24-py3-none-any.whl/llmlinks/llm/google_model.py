# %%
import os
import google.generativeai as genai

class GoogleLLM:

    def __init__(self, **kwargs):
        self.kwargs = kwargs    
        self.kwargs['model_name'] = self.kwargs.pop('model', None)
        self.genai = genai
        self.genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


    def __call__(self, input_text):
        model = self.genai.GenerativeModel(**self.kwargs)
        response = model.generate_content(input_text)
        output_text = response.text
        return output_text

if __name__ == "__main__":
    llm = GoogleLLM(model = 'gemini-1.5-flash')
    print(llm("Hello, world!"))


