from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage
from langchain.agents import create_agent
from pydantic import BaseModel

from app.utils import ai_settings
import streamlit as st


class CapitalInfo(BaseModel):
    name: str
    location: str
    vibe: str
    economy: str


st.title("Ai Agent")
llm_openai = ChatOpenAI(
    model=ai_settings.OPENAI_MODEL,
    api_key=ai_settings.OPENAI_API_KEY,
)

sys_prompt = """You are expect in providing the capital city of users request."""

agent = create_agent(
    model=llm_openai,
    system_prompt=sys_prompt,
    response_format=CapitalInfo,
)

question = st.text_input("Ask about a counties capital: ")

if question:
    response = agent.invoke({"messages": [HumanMessage(question)]})
    st.write(response["structured_response"])
