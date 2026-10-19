import pytest

from render_config import generate_configuration


def test_valid_configuration_renders():
    data = {
        "interfaces": [
            {
                "name": "GigabitEthernet3",
                "description": "Link-to-Core",
                "ip_address": "10.10.30.1",
                "subnet_mask": "255.255.255.252",
                "enabled": True
            }
        ]
    }

    result = generate_configuration(data)

    assert "interface GigabitEthernet3" in result
    assert "ip address 10.10.30.1 255.255.255.252" in result
    assert "no shutdown" in result


def test_invalid_ip_blocks_rendering():
    data = {
        "interfaces": [
            {
                "name": "GigabitEthernet3",
                "description": "Link-to-Core",
                "ip_address": "999.999.999.999",
                "subnet_mask": "255.255.255.252",
                "enabled": True
            }
        ]
    }

    with pytest.raises(ValueError, match="Invalid IP address"):
        generate_configuration(data)