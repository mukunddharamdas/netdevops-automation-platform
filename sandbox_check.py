
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
    "password": password,
    "ssh_strict": True,
    "system_host_keys": True,
}


# Initialize connection and validation state
connection = None
all_checks_passed = False
failures = []


try:
    # Establish connection
    connection = ConnectHandler(**device)
    print("Device connection successful")

    # Collect and parse device state
    output = connection.send_command(
        "show ip interface brief",
        use_textfsm=True
    )

    # Verify parsed data before trusting it
    validate_parsed_output(output)

    # Define expected network state
    required_interfaces = [
        "Vlan10",
        "Vlan20",
        "Loopback103"
    ]

    all_checks_passed = True

    # Validate required interfaces
    for interface_name in required_interfaces:

        result, reason = validate_interface(
            output,
            interface_name
        )

        print(f"{interface_name}: {result} - {reason}")

        if not result:
            all_checks_passed = False

            failures.append({
                "interface": interface_name,
                "reason": reason
            })


except NetmikoAuthenticationException:
    print("ERROR - Authentication failed")
    all_checks_passed = False


except NetmikoTimeoutException:
    print("ERROR - Connection timed out")
    all_checks_passed = False


except Exception as error:
    print(
        f"ERROR - Unexpected error: "
        f"{type(error).__name__}"
    )
    all_checks_passed = False


finally:
    if connection is not None:
        try:
            connection.disconnect()
            print("Device connection closed")

        except Exception as cleanup_error:
            print(
                f"ERROR - Connection cleanup failed: "
                f"{type(cleanup_error).__name__}"
            )
            all_checks_passed = False


# Final summary after connection cleanup
print("\n===== PRE-CHECK SUMMARY =====")

if all_checks_passed:
    print("Overall Result: PASSED")
else:
    print("Overall Result: FAILED")

print(f"Failed interface checks: {len(failures)}")


if failures:
    print("\nFailed Checks:")

    for failure in failures:
        print(
            f"{failure['interface']} - "
            f"{failure['reason']}"
        )


# Final deployment gate
print("\n===== DEPLOYMENT GATE =====")

if all_checks_passed:
    print("DEPLOYMENT ALLOWED")
    raise SystemExit(0)
else:
    print("DEPLOYMENT BLOCKED")
    raise SystemExit(1)
