from config_validation import validate_ip_address

def test_valid_ip_address():
    assert validate_ip_address("10.10.30.1") is True

def test_invalid_ip_address():
    assert validate_ip_address("999.999.999.999") is False