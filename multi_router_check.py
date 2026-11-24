
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
        "host": "192.0.2.10",
        "username": username,
        "password": password,
        "ssh_strict": True,
        "system_host_keys": True,
    },
    {
        "device_type": "cisco_ios",
        "host": "192.0.2.11",
        "username": username,
        "password": password,
        "ssh_strict": True,
        "system_host_keys": True,
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

    except Exception as error:
        print(
            f"{device['host']}: FAIL - "
            f"{type(error).__name__}"
        )
        return None


successful_devices = 0
failed_devices = 0

for device in devices:
    connection = connect_to_device(device)

    if connection is None:
        failed_devices += 1
        continue

    device_passed = False

    try:
        output = connection.send_command(
            "show ip interface brief"
        )

        if not output.strip():
            raise ValueError("Empty command output")

        print(f"{device['host']}: Command completed")
        print(f"Output size: {len(output)} characters")

        device_passed = True

    except Exception as error:
        print(f"{device['host']}: FAIL - Pre-check command failed")
        print(f"Error type: {type(error).__name__}")

    finally:
        try:
            connection.disconnect()
            print(f"{device['host']}: DISCONNECTED")

        except Exception as error:
            print(
                f"ERROR - Disconnect failed: "
                f"{type(error).__name__}"
            )
            device_passed = False

    if device_passed:
        successful_devices += 1
    else:
        failed_devices += 1


print("\n===== MULTI-DEVICE SUMMARY =====")
print(f"Total devices: {len(devices)}")
print(f"Successful devices: {successful_devices}")
print(f"Failed devices: {failed_devices}")

if failed_devices == 0:
    print("OVERALL RESULT: PASSED")
    raise SystemExit(0)

else:
    print("OVERALL RESULT: FAILED")
    raise SystemExit(1)
