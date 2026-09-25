import pytest
from network_validation import validate_parsed_output

def test_valid_parsed_output():

    test_output = [
        {
            "interface": "Vlan10",
            "status": "up",
            "proto": "up"
        }
    ]

    result = validate_parsed_output(test_output)
    assert result == True

def test_string_input_raises_value_error():
    test_output = "Vlan10 up up"

    with pytest.raises(ValueError):
        validate_parsed_output(test_output)

def test_list_of_strings_raises_value_error():
    test_output = [
        "Vlan10",
        "Vlan20"
    ]
    with pytest.raises(ValueError):
        validate_parsed_output(test_output)

def test_missing_proto_raises_value_error():
    test_output = [
        {
            "interface": "Vlan10",
            "status": "up"
        }
    ]

    with pytest.raises(
        ValueError,
        match="Structured parsing failed - missing key: proto"
    ):

        validate_parsed_output(test_output)