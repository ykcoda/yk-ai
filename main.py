from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_openai import OpenAIEmbeddings
from langgraph.checkpoint.memory import InMemorySaver
import streamlit as st

from document_loader import DocLoader


load_dotenv()

st.title("Memo AI")

agent = create_agent(model="gpt-5-nano")

dl = DocLoader(dir_path="./documents")


agent.invoke({"messages": [HumanMessage("Who is leading the premier league")]})
