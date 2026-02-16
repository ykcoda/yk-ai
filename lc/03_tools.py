from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage
from langchain.agents import create_agent
from pydantic import BaseModel
from lc.utils import ai_settings


class MathInfo(BaseModel):
    question: str
    answer: str


@tool
def square_root(x: float) -> float:
    """Calculate the square root of a number"""
    return x**0.5


model = ChatOpenAI(api_key=ai_settings.OPENAI_API_KEY, model=ai_settings.OPENAI_MODEL)


sys_prompt = """You are a math expect and you have tools that you can use to repond to users query"""
agent = create_agent(
    model=model, system_prompt=sys_prompt, tools=[square_root], response_format=MathInfo
)

question = input("Ask a math question: ")

if question:

    for token, metadata in agent.stream(
        {"messages": [HumanMessage(question)]}, stream_mode="messages"
    ):
        if token.content:
            print(token.content, end="", flush=True)
