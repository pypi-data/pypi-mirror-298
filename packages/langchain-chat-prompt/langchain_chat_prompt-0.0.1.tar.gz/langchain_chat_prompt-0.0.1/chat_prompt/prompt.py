from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain


class WelcomePrompt():
    def __init__(self, dynamic_var: list[str], datas: dict, question: dict, api_key: str, model_name: str, template: str) -> None:
        self.template = template
        self.dynamic_var = dynamic_var
        self.question = question
        self.datas = datas
        self.API_KEY = api_key
        self.MODEL = model_name

    def _create_template(self):
        prompt_template = PromptTemplate(
            input_variables=self.dynamic_var,
            template=self.template
        )
        return prompt_template

    def _format_and_create_message(self) -> dict:
        prompt_template = self._create_template()
        prompt_template.format(**self.datas)
        return prompt_template


class ExecuteLlm(WelcomePrompt):
    def __init__(self, dynamic_var: list[str], data: dict, question: dict, api_key: str, model_name: str, template: str) -> None:
        WelcomePrompt.__init__(
            self, dynamic_var, data, question, api_key, model_name, template)

    def run_prompt(self) -> dict:
        prompt_template = self._format_and_create_message()

        llms = ChatOpenAI(
            temperature=0.7,
            api_key=self.API_KEY,
            model=self.MODEL,
            max_tokens=1000,
        )
        welcome_chains = LLMChain(
            llm=llms,
            prompt=prompt_template,
            output_key="json_entities",
        )
        return welcome_chains.run(**self.question)
        # return {
        #     "template": self.template,
        #     "message": message_res
        # }
