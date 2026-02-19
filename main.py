from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.checkpoint.memory import InMemorySaver
import streamlit as st

from document_loader import DocLoader

load_dotenv()
st.title("Memo AI")

###############SPLITTER##########################
splitters = RecursiveCharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=800,
)

dl = DocLoader(dir_path="./documents")
splits = splitters.split_documents(dl.load_documents)


###############VECTOR_DB#######################
chroma_db = Chroma.from_documents(
    collection_name="yk_ai_collection",
    documents=splits,
    embedding=OpenAIEmbeddings(),
    persist_directory="./chroma_DB",
)

# results = chroma_db.similarity_search("solarwinds memo", k=100)

###############AGENTS##########################
agent = create_agent(
    model="gpt-5-nano",
)


agent.invoke({"messages": [HumanMessage("Who is leading the premier league")]})
