from langchain_openai import ChatOpenAI
from app.utils import ai_settings


llm_openai = ChatOpenAI(
    api_key=ai_settings.OPENAI_API_KEY,
    model=ai_settings.OPENAI_MODEL,
)
