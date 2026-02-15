from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage
from langchain.agents import create_agent

from app.utils import ai_settings
import streamlit as st

st.title("AI Agent")

llm_openai = ChatOpenAI(
    model=ai_settings.OPENAI_MODEL,
    api_key=ai_settings.OPENAI_API_KEY,
)

agent = create_agent(model=llm_openai)

human_msg = st.chat_input("Please ask a question: ")


def agent_response(human_msg: str):
    for token, metadata in agent.stream(
        {"messages": [HumanMessage(human_msg)]}, stream_mode="messages"
    ):
        if token.content:
            yield token.content


if human_msg:
    st.write_stream(agent_response(human_msg))
