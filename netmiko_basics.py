from netmiko import ConnectHandler

device = {
    "device_type": "cisco_ios",
    "host": "192.168.1.10",
    "username": "example-user",
    "password": "example-only",
}

print(device)
print(device["host"])