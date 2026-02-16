from langchain.agents import create_agent
from langchain.messages import HumanMessage
import langchain.tools
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from lc.utils import ai_settings


class CityInfo(BaseModel):
    name: str
    location: str
    vibe: str
    economt: str
    geography: str


model = ChatOpenAI(api_key=ai_settings.OPENAI_API_KEY, model=ai_settings.OPENAI_MODEL)

system_prompt = """you are an expect in geology. Give us some insite about a counties that is provied by the user"""

agent = create_agent(model=model, system_prompt=system_prompt, response_format=CityInfo)


for token, metadata in agent.stream(
    {"messages": [HumanMessage("Let me about the capital of Ghana.")]},
    stream_mode="messages",
):
    if token.content:
        print(token.content, end="", flush=True)

# response = agent.invoke(
#     {
#         "messages": [
#             HumanMessage(
#                 "What is the capital of Ghana? Provide us some of the cities vibe and info about its economy."
#             )
#         ]
#     }
# )

# print(response["messages"][-1].content)
