from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import HumanMessage
from netmiko import ConnectHandler  # type: ignore
from tavily import TavilyClient  # type: ignore

from fastapi import FastAPI, Body
from scalar_fastapi import get_scalar_api_reference

load_dotenv()

tavily_client = TavilyClient()


@tool
def web_search(query: str):
    """a tool that searches the web for current information if the model is unable to provide accurate info"""
    return tavily_client.search(query)


@tool
def network_device(ip: str, command: str):
    """Conencts to a network device by accepting an ip address and a command to execute on the device"""
    device = {
        "device_type": "cisco_ios",  # Change if different vendor
        "host": f"{ip}",
        "username": "y.kafreh",
        "password": "password.1password.1",
    }
    # Establish SSH connection
    connection = ConnectHandler(**device)
    # Enter enable mode (if required)
    connection.enable()
    # Run a command
    output = connection.send_command(command)
    return output


agent = create_agent(
    model="gpt-5-mini",
    tools=[web_search, network_device],
    system_prompt="""You are a network expert, based on the input/query from the user identify the ip address and command to execute on the network device by using the network_device tool. if the command submited is not correct try and get a valid command to execute and present a very nice output that is easily readable. Also i have a web_search tool that can give present info if the model can not provide that. """,
)

question = ""


app = FastAPI()


@app.post("/query/")
def query(query: str = Body(...)):
    print(query)
    response = agent.invoke({"messages": [HumanMessage(query)]})
    return response["messages"][-1].content


@app.get("/scalar", include_in_schema=False)
def scalar():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
    )

@app.get("/health")
def health():
    return {"status": "ok"}