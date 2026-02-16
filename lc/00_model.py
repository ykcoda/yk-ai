from langchain_openai import ChatOpenAI
from lc.utils import ai_settings


model = ChatOpenAI(api_key=ai_settings.OPENAI_API_KEY, model=ai_settings.OPENAI_MODEL)


for response in model.stream(
    "What is the capital of Ghana? Provide us some of the cities vibe and info about its economy"
):
    if response:
        print(response.content, end="", flush=True)
