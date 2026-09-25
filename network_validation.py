def validate_parsed_output(output):

    if not isinstance(output, list):
        raise ValueError(
            "Structured parsing failed - expected a list"
        )

    required_keys = [
        "interface",
        "status",
        "proto"
    ]

    for interface in output:
        if not isinstance(interface, dict):
            raise ValueError(
                "Structured parsing failed - expected dictionary records"
            )

        for key in required_keys:
            if key not in interface:
                raise ValueError(
                    f"Structured parsing failed - missing key: {key}"
                )
            
    return True


def validate_interface(output, interface_name):

    for interface in output:
        if interface["interface"] == interface_name:
            if interface["status"] == "up" and interface["proto"] == "up":
                return True, "interface is up/up"

            else:
                return False, (
                    f"status={interface['status']}, "
                    f"protocol={interface['proto']}"
                )

    return False, "interface not found"