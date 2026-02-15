from langgraph.checkpoint.memory import InMemorySaver
from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage
from langchain.agents import create_agent

from app.utils import ai_settings

import streamlit as st

st.title("AI Agent")


llm_openai = ChatOpenAI(
    api_key=ai_settings.OPENAI_API_KEY,
    model=ai_settings.OPENAI_MODEL,
)


# ---- Persistent Agent in session state ----
if "agent" not in st.session_state:
    st.session_state.agent = create_agent(
        model=llm_openai,
        checkpointer=InMemorySaver(),
    )
agent = st.session_state.agent

question = st.text_input("Ask a question: ")
config = {"configurable": {"thread_id": "1"}}

if question:
    response = agent.invoke(
        {"messages": [HumanMessage(content=question)]}, config=config
    )
    if response:
        st.write(response["messages"])
