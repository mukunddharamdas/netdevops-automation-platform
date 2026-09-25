import pytest
from network_validation import validate_interface

def test_interface_not_found():
    output = [
        {
            "interface": "Vlan10",
            "status": "up",
            "proto": "up"
        }
    ]
    result, reason = validate_interface(output, "Vlan999")

    assert result == False
    assert reason == "interface not found"

@pytest.mark.parametrize(
    "status, proto, expected_result",
    [
        ("up", "up", True),
        ("up", "down", False),
        ("down", "up", False),
        ("down", "down", False),
    ]
)

def test_interface_states(status, proto, expected_result):
    output = [
        {
            "interface": "Vlan10",
            "status": status,
            "proto": proto
        }
    ]

    result, reason = validate_interface(output, "Vlan10")
    assert result == expected_result