from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage
from langchain.agents import create_agent
from langchain.tools import tool

from app.utils import ai_settings
import streamlit as st
from typing import Dict
from tavily import TavilyClient  # type: ignore


st.title("AI Agent")


@tool("square_root", description="Calculate the square root of a provied number")
def tool1(x: float) -> float:
    return x**0.5


tavily_client = TavilyClient(api_key=ai_settings.TAVILY_API_KEY)


@tool
def web_search(query: str) -> Dict:
    """Search the web for information"""
    return tavily_client.search(query)


llm_openai = ChatOpenAI(
    model=ai_settings.OPENAI_MODEL,
    api_key=ai_settings.OPENAI_API_KEY,
)
agent = create_agent(model=llm_openai, tools=[web_search])


question = st.text_input("Ask any question: ")

if question:
    response = agent.invoke({"messages": [HumanMessage(question)]})

    if response:
        st.write(response["messages"])
