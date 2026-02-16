from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage
from langchain.tools import tool
from tavily import TavilyClient  # type: ignore

from app.utils import ai_settings


tavaly_client = TavilyClient(api_key=ai_settings.TAVILY_API_KEY)

llm_openai = ChatOpenAI(
    api_key=ai_settings.OPENAI_API_KEY,
    model=ai_settings.OPENAI_MODEL,
)


@tool
def web_search(query: str):
    """this will query the web for information"""
    return tavaly_client.search(query)


system_prompt = """You are personnal chef. the user will provide a list of ingredient left in their house. using the web search tool, search the web for recipess that can be made with the ingredients they have. 
return recipe suggestions and eventually the recipe instructions to the user, if requested.
"""


agent = create_agent(
    model=llm_openai,
    tools=[web_search],
    system_prompt=system_prompt,
)
