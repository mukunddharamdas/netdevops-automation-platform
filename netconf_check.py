from getpass import getpass

from ncclient import manager
from ncclient.transport.errors import SSHError

from netconf_validation import (
    retrieve_and_validate_iosxe_interface,
)

# Device information
host = "10.10.20.48"
port = 830

# Interface requirement
interface_name = "GigabitEthernet1"

# Get credentials at runtime
username = input("Username: ")
password = getpass("Password: ")

connection = None

try:
    # Establish NETCONF connection
    connection = manager.connect(
        host=host,
        port=port,
        username=username,
        password=password,
        hostkey_verify=False,
        device_params={"name": "iosxe"},
        timeout=30
    )

    print("NETCONF connection successful")

    # Retrieve live interface data and validate it
    result, reason = retrieve_and_validate_iosxe_interface(
        connection,
        interface_name
    )

    print("\n===== NETCONF PRE-CHECK =====")
    print(f"{interface_name}: {result} - {reason}")

    # Deployment gate
    if result:
        print("DEPLOYMENT ALLOWED")
    else:
        print("DEPLOYMENT BLOCKED")

except SSHError as error:
    print("\n===== NETCONF PRE-CHECK ERROR =====")
    print(f"ERROR - NETCONF SSH failure: {error}")
    print("DEPLOYMENT BLOCKED")

except ValueError as error:
    print("\n===== NETCONF PRE-CHECK ERROR =====")
    print(f"ERROR - {error}")
    print("DEPLOYMENT BLOCKED")

except Exception as error:
    print("\n===== NETCONF PRE-CHECK ERROR =====")
    print(f"ERROR - Unexpected failure: {error}")
    print("DEPLOYMENT BLOCKED")

finally:
    if connection is not None:
        try:
            connection.close_session()
            print("NETCONF connection closed")
        except Exception as cleanup_error:
            print(
                f"WARNING - NETCONF session cleanup failed: "
                f"{cleanup_error}"
            )
            