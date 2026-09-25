import requests
from getpass import getpass

host = "devnetsandboxiosxec9k.cisco.com"

username = input("Username: ")
password = getpass("Password: ")

url = f"https://{host}/restconf/data/ietf-interfaces:interfaces"

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
data = response.json()

interfaces = data["ietf-interfaces:interfaces"]["interface"]

# ----- VALIDATION STARTS HERE -----

def validate_interface_ip(interfaces, interface_name, expected_ip):

    for interface in interfaces:
        if interface["name"] == interface_name:
            addresses = interface["ietf-ip:ipv4"].get("address", [])

            for address in addresses:
                if address["ip"] == expected_ip:
                    return True, f"expected IP {expected_ip} found"

            return False, f"expected IP {expected_ip} not found"

    return False, f"interface {interface_name} not found"

result, reason = validate_interface_ip(
    interfaces,
    "Vlan10",
    "192.168.10.1"
)

if result:
    print(f"Vlan10: PASS - {reason}")
else:
    print(f"Vlan10: FAIL - {reason}")