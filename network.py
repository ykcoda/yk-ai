from dotenv import load_dotenv
from langchain.tools import tool
from langchain.agents import create_agent
from netmiko import ConnectHandler  # type: ignore
from langchain.messages import HumanMessage


load_dotenv()


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
    tools=[network_device],
    system_prompt="""You are a network expert, based on the input/query from the user identify the ip address and command to execute on the network device by using the network_device tool. if the command submited is not correct try and get a valid command to execute and present a very nice output that is easily readable""",
)

question = input("Send in any network command with the ip address: ")

while True:
    if question:
        for message, metadata in agent.stream(
            {"messages": [HumanMessage(question)]}, stream_mode="messages"
        ):
            if message.content:
                print(message.content, end="", flush=True)
