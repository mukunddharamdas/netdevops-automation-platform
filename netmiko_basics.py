from netmiko import ConnectHandler

device = {
    "device_type": "cisco_ios",
    "host": "192.168.1.10",
    "username": "example-user",
    "password": "example-only",
}

print(f"Device type: {device['device_type']}")
print(f"Device host: {device['host']}")