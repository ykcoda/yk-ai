from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage
from langchain.tools import tool
from tavily import TavilyClient  # type: ignore

load_dotenv()

tavily_client = TavilyClient()


@tool
def web_search(query: str):
    """searches the internet for information based on user query"""
    return tavily_client.search(query)


agent = create_agent(model="gpt-5-nano")


response = agent.invoke(
    {"messages": [HumanMessage("Who is the president of ghana as at 2026")]}
)
print(response["messages"][-1].content)
