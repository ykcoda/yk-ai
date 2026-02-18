import httpx
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
import tavily  # type: ignore

load_dotenv()


@tool(
    "get_weather",
    description="Return weather information for a given city",
    return_direct=False,
)
def get_weather(city: str):
    response = httpx.get(f"https://wttr.in/{city}?format=j1")
    return response.json()


agent = create_agent(model="gpt-5-nano")
