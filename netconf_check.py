from getpass import getpass

from ncclient import manager
from ncclient.transport.errors import SSHError

from netconf_validation import retrieve_and_validate_interface

host = "devnetsandboxiosxec9k.cisco.com"

username = input("Username: ")
password = getpass("Password: ")

connection = None

try:
    connection = manager.connect(
        host=host,
        port=830,
        username=username,
        password=password,
        hostkey_verify=False,
        device_params={"name": "iosxe"},
        timeout=10
    )

    print("NETCONF connection successful")

    result, reason = retrieve_and_validate_interface(
        connection,
        "Vlan20"
    )
    
    print()
    print("===== NETCONF PRE-CHECK =====")
    print(f"Vlan20: {result} - {reason}")

    if result:
        print("DEPLOYMENT ALLOWED")
    else:
        print("DEPLOYMENT BLOCKED")

except SSHError as error:
    print()
    print("===== NETCONF PRE-CHECK ERROR =====")
    print(f"ERROR - NETCONF SSH failure: {error}")
    print("DEPLOYMENT BLOCKED")

except ValueError as error:
    print()
    print("===== NETCONF PRE-CHECK ERROR =====")
    print(f"ERROR - Invalid or incomplete NETCONF data: {error}")
    print("DEPLOYMENT BLOCKED")

except Exception as error:
    print()
    print("===== NETCONF PRE-CHECK ERROR =====")
    print(f"ERROR - Unexpected NETCONF error: {error}")
    print("DEPLOYMENT BLOCKED")

finally:
    if connection is not None:
        try:
            connection.close_session()
        except Exception as cleanup_error:
            print(
                f"WARNING - NETCONF session cleanup failed: "
                f"{cleanup_error}"
            )