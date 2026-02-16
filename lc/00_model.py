from langchain_openai import ChatOpenAI

from pprint import pprint
from lc.utils import ai_settings

llm_openai = ChatOpenAI(
    api_key=ai_settings.OPENAI_API_KEY,
    model=ai_settings.OPENAI_MODEL,
    temperature=0.1,
)

response = llm_openai.invoke("What is the capital of the Moon")

pprint(response)
