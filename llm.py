import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()


def load_document(docs_path: str):
    documents = []

    for filename in os.listdir(docs_path):
        file_path = os.path.join(docs_path, filename)

        if filename.endswith(".docx"):
            loader = Docx2txtLoader(file_path)
        elif filename.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        else:
            print(f"Unsupported Document: {filename}")
            continue
        documents.extend(loader.load())
    return documents


splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)
documents = load_document("./documents")

print(f"Documents loaded: {len(documents)}")
splits = splitter.split_documents(documents)

embeddings_function = OpenAIEmbeddings()

# embeddings = embeddings_function.embed_documents(
#     [split.page_content for split in splits]
# )

# print(embeddings)

vector_db = Chroma.from_documents(
    collection_name="my_collections",
    embedding=embeddings_function,
    documents=splits,
    persist_directory="./chroma_db",
)

# Perform similarity search
# query = "When is the renewal of commvault"

# search_result = vector_db.similarity_search(query, k=2)

# for i, result in enumerate(search_result, 1):
#     print(f"result: {i}")
#     print(f"source: {result.metadata.get('source', 'Unknown')}")
#     print(f"result: {result.page_content}")


# retriever = vector_db.as_retriever(search_kwargs={"k": 2})

query = "approver the commvault memo"

results = vector_db.similarity_search(query, k=3)
print(results[:2])

llm_openai = ChatOpenAI()

prompt = ChatPromptTemplate.from_template(
    """Answer the following questions based on the context provided. 
                                          think step by step before proving a detailed answer. 
                                          I will tip you $1000 if the user finds it helpdful.
                                          <context>
                                          {context}
                                          </context>
                                          Question: {input}"""
)
