import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.agents import create_agent
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_core.tools import create_retriever_tool
from langchain.messages import HumanMessage

load_dotenv()


def get_documents(directory_path: str):
    documents = []
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif filename.endswith(".docx"):
            loader = Docx2txtLoader(file_path)  # type: ignore
        else:
            print(f"Unsupported file: {filename}")
            continue
        documents.extend(loader.load())
    return documents


documents = get_documents("./documents")

spliters = RecursiveCharacterTextSplitter(
    chunk_size=5000,
    chunk_overlap=1500,
)

splits = spliters.split_documents(documents=documents)

vector_db = Chroma.from_documents(
    collection_name="rag_collection",
    documents=splits,
    embedding=OpenAIEmbeddings(),
    persist_directory="./chromaDB",
)

# print(vector_db.similarity_search("who approved the commvault memo", k=3))
# print(vector_db.similarity_search("when is the next commvault renewal", k=3))


retriever = vector_db.as_retriever(search_kwargs={"k": 500})

retriever_tool = create_retriever_tool(
    retriever, name="kb_search", description="Search the database for relevant info"
)


agent = create_agent(
    model="gpt-5-nano",
    tools=[retriever_tool],
    system_prompt=(
        "You are a helpful assistant. first call is kb_search to retrieve context, then answer accuratly, maybe you have to use it multiple times before answering "
    ),
)
question = input("Ask a question: ")

if question:
    response = agent.invoke({"messages": [HumanMessage(question)]})
    print(response["messages"][-1].content)
