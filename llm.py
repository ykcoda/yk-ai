from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from pprint import pprint

load_dotenv()


text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)

docx_loader = Docx2txtLoader("./docs/doc3.docx")
document = docx_loader.load()

splits = text_splitter.split_documents(document)

pprint(len(splits))

model = ChatOpenAI()
