from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate

# from langchain_core.globals import set_debug

from app.utils import ai_settings


# set_debug(True)


class LLMConnector:
    def __init__(self):
        self.openai = ChatOpenAI(
            api_key=ai_settings.OPENAI_API_KEY, model=ai_settings.OPENAI_MODEL
        )
        self.ollama = ChatOllama(model=ai_settings.OLLAMA_MODEL)

    def query(self, question, llm="openai"):
        client = getattr(self, llm)

        if client is None:
            raise ValueError(f"{client} not configured")

        response = client.invoke(question)
        return response.content

    def promptTemplate(
        self, country: str, no_of_paraghaphs: int, language: str, llm="openai"
    ):
        client = getattr(self, llm)

        if client is None:
            raise ValueError(f"{client} not configured")

        prompt_template = PromptTemplate(
            input_variables=["country", "no_of_paraghaphs", "language"],
            template="""You are an expert in traditional cuisines.
You provide information about a specific dish from a specific country.
Avoid giving information about fictional places. If the country is fictional
or non-existent answer: I don't know.
Answer the question: What is the traditional cuisine of {country}?
Answer in {no_of_paraghaphs} short paras in {language}""",
        )

        response = client.invoke(
            prompt_template.format(
                country=country, no_of_paraghaphs=no_of_paraghaphs, language=language
            )
        )
        return response.content


llm_connector = LLMConnector()
# question = input("Please ask a question: ")
# print(llm_connector.query(question))
