import yaml
from getpass import getpass

from ncclient import manager
from ncclient.transport.errors import SSHError

from netconf_validation import (
    retrieve_and_validate_iosxe_interface,
)


# Load inventory
with open("inventory.yaml", "r") as file:
    data = yaml.safe_load(file)

devices = data["devices"]

# Get credentials once
username = input("Username: ")
password = getpass("Password: ")


# Overall result across all devices
all_devices_passed = True


for device in devices:
    hostname = device["hostname"]
    host = device["host"]
    port = device["port"]
    interfaces = device["interfaces"]

    connection = None

    print(f"\n===== DEVICE: {hostname} =====")

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
        print("\n===== NETCONF PRE-CHECK =====")

        device_checks_passed = True

        for interface in interfaces:
            interface_name = interface["name"]
            expected_status = interface["expected_status"]

            result, reason = retrieve_and_validate_iosxe_interface(
                connection,
                interface_name,
                expected_status
            )

            print(
                f"{interface_name}: "
                f"{result} - {reason}"
            )

            if not result:
                device_checks_passed = False
                all_devices_passed = False

        if device_checks_passed:
            print(f"{hostname}: ALL CHECKS PASSED")
        else:
            print(f"{hostname}: CHECKS FAILED")

    except SSHError as error:
        print(f"ERROR - NETCONF SSH failure: {error}")
        all_devices_passed = False

    except ValueError as error:
        print(f"ERROR - {error}")
        all_devices_passed = False

    except Exception as error:
        print(f"ERROR - Unexpected failure: {error}")
        all_devices_passed = False

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


print("\n===== OVERALL DEPLOYMENT GATE =====")

if all_devices_passed:
    print("DEPLOYMENT ALLOWED")
else:
    print("DEPLOYMENT BLOCKED")