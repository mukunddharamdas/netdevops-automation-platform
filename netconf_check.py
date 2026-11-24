
import yaml
from getpass import getpass

from ncclient import manager
from ncclient.transport.errors import SSHError

from inventory_validation import validate_inventory

from netconf_validation import (
    retrieve_and_validate_iosxe_interface,
)


# Load and validate inventory
try:
    with open("inventory.yaml", "r") as file:
        data = yaml.safe_load(file)

    devices = validate_inventory(data)

except (OSError, yaml.YAMLError):
    print("ERROR - Unable to read or parse inventory")
    print("DEPLOYMENT BLOCKED")
    raise SystemExit(1)

except ValueError as error:
    print(f"ERROR - {error}")
    print("DEPLOYMENT BLOCKED")
    raise SystemExit(1)


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
            hostkey_verify=True,
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
            print(f"{hostname}: ALL INTERFACE CHECKS PASSED")
        else:
            print(f"{hostname}: INTERFACE CHECKS FAILED")

    except SSHError as error:
        print(
            f"ERROR - NETCONF SSH failure: "
            f"{type(error).__name__}"
        )
        all_devices_passed = False

    except ValueError as error:
        print(
            f"ERROR - Validation failure: "
            f"{type(error).__name__}"
        )
        all_devices_passed = False

    except Exception as error:
        print(
            f"ERROR - Unexpected failure: "
            f"{type(error).__name__}"
        )
        all_devices_passed = False

    finally:
        if connection is not None:
            try:
                connection.close_session()
                print("NETCONF connection closed")

            except Exception as cleanup_error:
                print(
                    f"ERROR - NETCONF session cleanup failed: "
                    f"{type(cleanup_error).__name__}"
                )
                all_devices_passed = False


print("\n===== OVERALL DEPLOYMENT GATE =====")

if all_devices_passed:
    print("DEPLOYMENT ALLOWED")
    raise SystemExit(0)
else:
    print("DEPLOYMENT BLOCKED")
    raise SystemExit(1)
