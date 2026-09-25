import requests
from getpass import getpass

host = "devnetsandboxiosxec9k.cisco.com"

username = input("Username: ")
password = getpass("Password: ")

url = (
    f"https://{host}/restconf/data/"
    "Cisco-IOS-XE-interfaces-oper:interfaces"
)

headers = {
    "Accept": "application/yang-data+json"
}

response = requests.get(
    url,
    headers=headers,
    auth=(username, password),
    timeout=10,
    verify=False
)

print(f"Status code: {response.status_code}")
response.raise_for_status()
print(response.text)