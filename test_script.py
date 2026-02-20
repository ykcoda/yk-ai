from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.tools.retriever import create_retriever_tool
from langgraph.checkpoint.memory import InMemorySaver
import streamlit as st

from document_loader import DocLoader

load_dotenv()
st.title("FBL Memo AI")

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
retriever = chroma_db.as_retriever(search_kwargs={"k": 3})
retriever_tool = create_retriever_tool(
    retriever=retriever,
    name="kb_search",
    description="Search the doc knowledge for information",
)

###############AGENTS##########################
agent = create_agent(
    model="gpt-5-mini",
    tools=[retriever_tool],
    system_prompt="""You are helpful assistant who can assist get accurate information about memo from the kb_search tool upon users request or query.""",
    checkpointer=InMemorySaver(),
)

question = st.chat_input("Query: ")

if question:
    config = {"configurable": {"thread_id": "1"}}
    response = agent.invoke({"messages": [HumanMessage(question)]}, config=config)
    st.write(response["messages"][-1].content)
