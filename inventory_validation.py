def validate_inventory(data):
    """Validate inventory structure and required fields."""

    if not isinstance(data, dict):
        raise ValueError("Inventory must be a dictionary")

    if "devices" not in data:
        raise ValueError("Inventory is missing the devices field")

    devices = data["devices"]

    if not isinstance(devices, list):
        raise ValueError("Devices must be a list")

    if not devices:
        raise ValueError("Device inventory is empty")

    # Validate individual devices
    for device in devices:

        if not isinstance(device, dict):
            raise ValueError("Each device must be a dictionary")

        # Validate required text fields
        for field in ("hostname", "host"):
            value = device.get(field)

            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"Invalid or missing {field}")

        # Validate connection port
        port = device.get("port")

        if type(port) is not int or not 1 <= port <= 65535:
            raise ValueError(
                f"{device['hostname']} has an invalid port"
            )

        # Validate interface list
        interfaces = device.get("interfaces")

        if not isinstance(interfaces, list) or not interfaces:
            raise ValueError(
                f"{device['hostname']} requires a non-empty interface list"
            )

        # Validate individual interfaces
        for interface in interfaces:

            if not isinstance(interface, dict):
                raise ValueError(
                    "Each interface must be a dictionary"
                )

            for field in ("name", "expected_status"):
                value = interface.get(field)

                if not isinstance(value, str) or not value.strip():
                    raise ValueError(
                        f"Invalid or missing interface {field}"
                    )

    return devices

import pytest

from inventory_validation import validate_inventory


def test_valid_inventory():
    data = {
        "devices": [
            {
                "hostname": "Router1",
                "host": "192.0.2.10",
                "port": 830,
                "interfaces": [
                    {
                        "name": "GigabitEthernet1",
                        "expected_status": "up"
                    }
                ]
            }
        ]
    }

    result = validate_inventory(data)

    assert result == data["devices"]


def test_empty_inventory():
    data = {"devices": []}

    with pytest.raises(
        ValueError,
        match="Device inventory is empty"
    ):
        validate_inventory(data)