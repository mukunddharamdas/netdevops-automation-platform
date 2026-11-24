
import requests
from getpass import getpass


def validate_interface_ip(
    interfaces,
    interface_name,
    expected_ip
):
    for interface in interfaces:

        if interface["name"] == interface_name:

            addresses = interface.get(
                "ietf-ip:ipv4", {}
            ).get("address", [])

            for address in addresses:
                if address["ip"] == expected_ip:
                    return True, "Expected IP address found"

            return False, "Expected IP address not found"

    return False, "Required interface not found"


if __name__ == "__main__":

    host = "devnetsandboxiosxec9k.cisco.com"

    username = input("Username: ")
    password = getpass("Password: ")

    url = f"https://{host}/restconf/data/ietf-interfaces:interfaces"

    headers = {
        "Accept": "application/yang-data+json"
    }

    all_checks_passed = False

    try:
        response = requests.get(
            url,
            headers=headers,
            auth=(username, password),
            timeout=10,
            verify=True
        )

        print(f"Status code: {response.status_code}")

        response.raise_for_status()

        data = response.json()

        interfaces = data["ietf-interfaces:interfaces"]["interface"]

        result, reason = validate_interface_ip(
            interfaces,
            "Vlan10",
            "192.168.10.1"
        )

        if result:
            print(f"Vlan10: PASS - {reason}")
            all_checks_passed = True
        else:
            print(f"Vlan10: FAIL - {reason}")

    except requests.exceptions.SSLError:
        print("ERROR - TLS certificate verification or handshake failed")

    except requests.exceptions.Timeout:
        print("ERROR - RESTCONF request timed out")

    except requests.exceptions.HTTPError as error:
        print(f"ERROR - HTTP failure: {type(error).__name__}")

    except requests.exceptions.JSONDecodeError:
        print("ERROR - Invalid JSON response")

    except requests.exceptions.RequestException as error:
        print(f"ERROR - Request failed: {type(error).__name__}")

    except (KeyError, TypeError, AttributeError):
        print("ERROR - Unexpected RESTCONF response structure")

    except Exception as error:
        print(f"ERROR - Unexpected failure: {type(error).__name__}")


    print("\n===== DEPLOYMENT GATE =====")

    if all_checks_passed:
        print("DEPLOYMENT ALLOWED")
        raise SystemExit(0)
    else:
        print("DEPLOYMENT BLOCKED")
        raise SystemExit(1)
