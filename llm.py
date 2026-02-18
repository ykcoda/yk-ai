import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

load_dotenv()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)


embeddings = OpenAIEmbeddings()


def document_loader(docs_path: str):
    documents: list[str] = []

    for filename in os.listdir(docs_path):
        file_path = os.path.join(docs_path, filename)

        if filename.endswith(".docx"):
            loader = Docx2txtLoader(file_path)
        elif filename.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        else:
            print(f"Unsupported file type: {file_path}")
            continue
        documents.extend(loader.load())
    return documents


documents = document_loader("./documents")


splits = splitter.split_documents(documents)


document_embeddings = embeddings.embed_documents(
    [split.page_content for split in splits]
)

print(f"Enbiddings Size: {len(document_embeddings)}")


collection_name = "my_collection"
vector_db = Chroma.from_documents(
    documents=splits,
    embedding=embeddings,
    collection_name=collection_name,
    persist_directory="./chroma_db",
)
print("Vector db is created")
