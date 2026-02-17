from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

load_dotenv()

model = ChatOpenAI()

prompt_msg = PromptTemplate(
    input_variables=["topic"],
    template="""Tell me a short joke about {topic}""",
)

# chain = model | output_parser

# chain.invoke("who is currently leading the premier league")

chain = prompt_msg | model

chain.invoke({"topic": "football"})
