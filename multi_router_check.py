from getpass import getpass

from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException
)

username = input("Username: ")
password = getpass("Password: ")

devices = [
    {
        "device_type": "cisco_ios",
        "host": "192.168.1.10",
        "username": username,
        "password": password
    },
    {
        "device_type": "cisco_ios",
        "host": "192.168.1.11",
        "username": username,
        "password": password
    }
]

def connect_to_device(device):
    try:
        connection = ConnectHandler(**device)
        print(f"{device['host']}: CONNECTED")
        return connection

    except NetmikoTimeoutException:
        print(f"{device['host']}: FAIL - Connection timeout")
        return None

    except NetmikoAuthenticationException:
        print(f"{device['host']}: FAIL - Authentication failed")
        return None


for device in devices:
    connection = connect_to_device(device)

    if connection is None:
        continue

    try:
        output = connection.send_command("show ip interface brief")
        print(output)

    except Exception as error:
        print(f"{device['host']}: FAIL - Pre-check command failed")
        print(error)

    finally:
        connection.disconnect()