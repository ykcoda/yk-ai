from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain.tools import tool
from netmiko import ConnectHandler  # type: ignore

import streamlit as st
from tavily import TavilyClient  # type: ignore


st.title("Network Command Assistant")

load_dotenv()


tavily_client = TavilyClient()


@tool
def web_search(query: str):
    """Use this if the agent want to search websites for info"""
    return tavily_client.search(query)


@tool
def network_device(ip: str, command: str):
    """Tool to execute commands on network devices by IP."""

    cisco_router = {
        "device_type": "cisco_ios",  # For IOS routers
        "host": f"{ip}",  # Router IP address
        "username": "l.hammond",  # Your SSH username
        "password": "0558401840Nii*&@!!",  # Optional, if you want to enter enable mode
    }
    # Connect to the router
    net_connect = ConnectHandler(**cisco_router)
    net_connect.enable()
    output = net_connect.send_command(command)

    return f"{output}"


model = ChatOpenAI()

system_prompt = """You are a network engineer. User can pass in one or more ip addresses. with the ips, query the bgp status of each of the devices. """


agent = create_agent(
    model=model, tools=[network_device, web_search], system_prompt=system_prompt
)

question = st.chat_input("Ask a question about a network device")

output_placeholder = st.empty()

if question:
    # Create a string to accumulate the streamed tokens
    output_text = ""

    # Stream from LangChain agent
    for token, metadata in agent.stream(
        {"messages": [HumanMessage(content=question)]}, stream_mode="messages"
    ):
        if token.content:
            output_text += token.content
            # Update the Streamlit placeholder in real-time
            output_placeholder.text(output_text)
