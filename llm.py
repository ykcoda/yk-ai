from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage, SystemMessage

load_dotenv()

model = ChatOpenAI()


# chain = model | output_parser

# chain.invoke("who is currently leading the premier league")


model.invoke(
    [
        HumanMessage("Tell me about programming"),
        SystemMessage("You are helpfull assistance who tells joke"),
    ]
)
