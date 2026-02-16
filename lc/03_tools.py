from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage
from langchain.agents import create_agent

from pydantic import BaseModel
from tavily import TavilyClient

from lc.utils import ai_settings
from pprint import pprint


tavily_client = TavilyClient(api_key=ai_settings.TAVILY_API_KEY)


class MathInfo(BaseModel):
    question: str
    answer: str


@tool
def square_root(x: float) -> float:
    """Calculate the square root of a number"""
    return x**0.5


@tool
def web_search(query: str):
    """Searches the web for current information"""
    return tavily_client.search(query=query)


model = ChatOpenAI(api_key=ai_settings.OPENAI_API_KEY, model=ai_settings.OPENAI_MODEL)


sys_prompt = """You are an expect in surfing the web for recent infomation and you have tools that you can use to repond to users query"""
agent = create_agent(model=model, system_prompt=sys_prompt, tools=[web_search])

question = input("Ask any question: ")

if question:
    for token, metadata in agent.stream(
        {"messages": [HumanMessage(question)]}, stream_mode="messages"
    ):
        if token.content:
            print(token.content, end="", flush=True)

    # for token, metadata in agent.stream(
    #     {"messages": [HumanMessage(question)]}, stream_mode="messages"
    # ):
    #     if token.content:
    #         print(token.content, end="", flush=True)
