import ipaddress

def validate_ip_address(address):
    try:
        ipaddress.IPv4Address(address)
        return True

    except ipaddress.AddressValueError:
        return False