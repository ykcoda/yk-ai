from netmiko import ConnectHandler  # type: ignore


class NetworkConfig:

    def __init__(self, device: dict):
        self.connect = ConnectHandler(**device)

    def run_command(self, command: str):
        return self.connect.send_command(command)


ip_address = input("IP Address: ")
command = input("Command#: ")

device = {
    "device_type": "cisco_ios",
    "host": f"{ip_address}",
    "username": "y.kafreh",
    "password": "password.1password.1",
}


net_conf = NetworkConfig(device)

output = net_conf.run_command(f"{command}")

print(output)
