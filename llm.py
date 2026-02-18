from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

model = ChatOpenAI()


# chain = model | output_parser

# chain.invoke("who is currently leading the premier league")

template = ChatPromptTemplate(
    [
        ("system", "You are a helpful assistant that tells kokes"),
        ("human", "tell me about a {topic}"),
    ]
)


template.invoke({"topic": "python"})
