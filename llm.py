import httpx
from dataclasses import dataclass

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool, ToolRuntime
from langchain.messages import HumanMessage

from langgraph.checkpoint.memory import InMemorySaver
import tavily  # type: ignore

load_dotenv()


@dataclass
class Context:
    user_id: str


@dataclass
class ResponseFormat:
    summary: str
    temperature_celsius: float
    temperature_fahrenheit: float
    humidity: float


@tool(
    "get_weather",
    description="Return weather information for a given city",
    return_direct=False,
)
def get_weather(city: str):
    response = httpx.get(f"https://wttr.in/{city}?format=j1")
    return response.json()


@tool("locate_user", description="Look up a user's city based on the context")
def locate_user(runtime: ToolRuntime[Context]):
    match runtime.context.user_id:
        case "ABC123":
            return "Accra"
        case "XYZ456":
            return "Sunderland"
        case "HJK11":
            return "Paris"
        case _:
            return "Unknown"


model = init_chat_model("gpt-5-nano", temperature=0.3)

agent = create_agent(
    model=model,
    tools=[get_weather, locate_user],
    system_prompt="You are a helpful weather assistance who always cracks jokes whiles remaining helpful",
    response_format=ResponseFormat,
    context_schema=Context,
    checkpointer=InMemorySaver(),
)

config = {"configurable": {"thread_id": 1}}

response = agent.invoke(
    {"messages": [HumanMessage("What is the weather like in Sunderland now")]},
    config=config,
    context=Context(user_id="ABC123"),
)
print(response["structured_response"].summary)


response = agent.invoke(
    {"messages": [HumanMessage("Is this weather normal?")]},
    config=config,
    context=Context(user_id="ABC123"),
)

print(response["structured_response"].summary)
