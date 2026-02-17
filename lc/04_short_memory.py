from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from utils import ai_settings
from pprint import pprint


model = ChatOpenAI(api_key=ai_settings.OPENAI_API_KEY, model=ai_settings.OPENAI_MODEL)
agent = create_agent(model=model, checkpointer=InMemorySaver())


while True:
    question = input("Ask any question: ")
    config = {"configurable": {"thread_id": "1"}}

    if question:
        response = agent.invoke({"messages": [HumanMessage(question)]}, config=config)  # type: ignore
        pprint(response)
