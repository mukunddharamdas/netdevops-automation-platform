import pytest

from inventory_validation import validate_inventory


# Reusable valid inventory fixture
@pytest.fixture
def valid_inventory():
    return {
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


# Test valid inventory
def test_valid_inventory(valid_inventory):
    result = validate_inventory(valid_inventory)

    assert result == valid_inventory["devices"]


# Test empty device inventory
def test_empty_inventory():
    data = {"devices": []}

    with pytest.raises(
        ValueError,
        match="Device inventory is empty"
    ):
        validate_inventory(data)


# Test invalid inventory structures
@pytest.mark.parametrize(
    "data, expected_error",
    [
        (
            None,
            "Inventory must be a dictionary"
        ),
        (
            {"routers": []},
            "Inventory is missing the devices field"
        ),
        (
            {"devices": "Router1"},
            "Devices must be a list"
        ),
        (
            {"devices": ["Router1"]},
            "Each device must be a dictionary"
        ),
        (
            {"devices": [{}]},
            "Invalid or missing hostname"
        ),
    ]
)
def test_invalid_inventory(data, expected_error):
    with pytest.raises(ValueError, match=expected_error):
        validate_inventory(data)


# Test invalid connection ports
@pytest.mark.parametrize(
    "invalid_port",
    ["830", 0, -1, 65536, None, True]
)
def test_invalid_port(valid_inventory, invalid_port):
    valid_inventory["devices"][0]["port"] = invalid_port

    with pytest.raises(ValueError, match="invalid port"):
        validate_inventory(valid_inventory)


# Test invalid interface lists
@pytest.mark.parametrize(
    "invalid_interfaces",
    [[], None, "GigabitEthernet1", {}]
)
def test_invalid_interface_list(
    valid_inventory,
    invalid_interfaces
):
    valid_inventory["devices"][0]["interfaces"] = (
        invalid_interfaces
    )

    with pytest.raises(
        ValueError,
        match="requires a non-empty interface list"
    ):
        validate_inventory(valid_inventory)


# Test missing interfaces field
def test_missing_interfaces(valid_inventory):
    del valid_inventory["devices"][0]["interfaces"]

    with pytest.raises(
        ValueError,
        match="requires a non-empty interface list"
    ):
        validate_inventory(valid_inventory)


# Test invalid individual interface
def test_invalid_interface_entry(valid_inventory):
    valid_inventory["devices"][0]["interfaces"] = [
        "GigabitEthernet1"
    ]

    with pytest.raises(
        ValueError,
        match="Each interface must be a dictionary"
    ):
        validate_inventory(valid_inventory)


# Test invalid interface fields
@pytest.mark.parametrize(
    "field, invalid_value",
    [
        ("name", ""),
        ("name", None),
        ("name", 123),
        ("expected_status", ""),
        ("expected_status", None),
        ("expected_status", 123),
    ]
)
def test_invalid_interface_field(
    valid_inventory,
    field,
    invalid_value
):
    interface = valid_inventory["devices"][0]["interfaces"][0]

    interface[field] = invalid_value

    with pytest.raises(
        ValueError,
        match=f"Invalid or missing interface {field}"
    ):
        validate_inventory(valid_inventory)


# Test missing host field
def test_missing_host(valid_inventory):
    del valid_inventory["devices"][0]["host"]

    with pytest.raises(
        ValueError,
        match="Invalid or missing host"
    ):
        validate_inventory(valid_inventory)


# Test multiple devices with one invalid device
def test_multiple_devices_one_invalid(valid_inventory):
    valid_inventory["devices"].append(
        {
            "hostname": "Router2",
            "host": "192.0.2.11",
            "port": 830,
            "interfaces": []
        }
    )

    with pytest.raises(
        ValueError,
        match="Router2 requires a non-empty interface list"
    ):
        validate_inventory(valid_inventory)
