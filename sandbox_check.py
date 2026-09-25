from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException
)
from getpass import getpass
from network_validation import (
    validate_parsed_output,
    validate_interface
)

# Get credentials securely at runtime
username = input("Enter the username: ")
password = getpass("Enter the password: ")

# Cisco DevNet sandbox device
device = {
    "device_type": "cisco_ios",
    "host": "devnetsandboxiosxec9k.cisco.com",
    "username": username,
    "password": password
}

# No connection exists yet
connection = None

try:
    # Connect
    connection = ConnectHandler(**device)

    # Collect and parse device state
    output = connection.send_command(
        "show ip interface brief",
        use_textfsm=True
    )

    # Verify parsed data BEFORE trusting it
    validate_parsed_output(output)

    # Define expected network state
    required_interfaces = [
        "Vlan10",
        "Vlan20",
        "Loopback103"
    ]

    all_checks_passed = True
    failures = []

    # Validate required interfaces
    for interface_name in required_interfaces:

        result, reason = validate_interface(
            output,
            interface_name
        )

        print(f"{interface_name}: {result} - {reason}")

        if result == False:
            all_checks_passed = False

            failures.append({
                "interface": interface_name,
                "reason": reason
            })

    # Summary
    print()
    print("===== PRE-CHECK SUMMARY =====")

    if all_checks_passed:
        print("Overall Result: PASSED")
    else:
        print("Overall Result: FAILED")

    print(f"Total Failures: {len(failures)}")

    if len(failures) > 0:
        print()
        print("Failed Checks:")

        for failure in failures:
            print(
                f"{failure['interface']} - "
                f"{failure['reason']}"
            )

    if all_checks_passed:
        print()
        print("DEPLOYMENT ALLOWED")
    else:
        print()
        print("DEPLOYMENT BLOCKED")

except NetmikoAuthenticationException:
    print()
    print("===== PRE-CHECK ERROR =====")
    print("ERROR - Authentication failed")
    print("DEPLOYMENT BLOCKED")

except NetmikoTimeoutException:
    print()
    print("===== PRE-CHECK ERROR =====")
    print("ERROR - Connection timed out")
    print("DEPLOYMENT BLOCKED")

except Exception as error:
    print()
    print("===== PRE-CHECK ERROR =====")
    print(f"ERROR - Unexpected error: {error}")
    print("DEPLOYMENT BLOCKED")


finally:
    if connection is not None:
        connection.disconnect()