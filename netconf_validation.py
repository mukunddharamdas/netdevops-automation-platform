import xml.etree.ElementTree as ET

def parse_netconf_xml(xml_data):
    try:
        root = ET.fromstring(xml_data)
        return root

    except ET.ParseError as error:
        raise ValueError(
            f"Invalid NETCONF XML: {error}"
        )

def validate_oper_status(root, interface_name):

    namespace = {
        "if": "urn:ietf:params:xml:ns:yang:ietf-interfaces"
    }

    # Support both namespaced NETCONF XML
    # and our simple non-namespaced test XML.
    interfaces = root.findall(".//if:interface", namespace)

    if not interfaces:
        interfaces = root.findall(".//interface")

    for interface in interfaces:

        name_element = interface.find("if:name", namespace)

        if name_element is None:
            name_element = interface.find("name")

        if name_element is None:
            raise ValueError(
                "NETCONF validation failed - missing interface name"
            )

        if name_element.text == interface_name:

            status_element = interface.find(
                "if:oper-status",
                namespace
            )

            if status_element is None:
                status_element = interface.find("oper-status")

            if status_element is None:
                raise ValueError(
                    f"NETCONF validation failed - "
                    f"missing oper-status for {interface_name}"
                )

            if status_element.text == "up":
                return True, "operational status is up"

            return False, (
                f"operational status is {status_element.text}"
            )

    return False, f"interface {interface_name} not found"

def retrieve_and_validate_interface(
    connection,
    interface_name
):
    interface_filter = f"""
    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
            <name>{interface_name}</name>
        </interface>
    </interfaces>
    """

    reply = connection.get(
        filter=("subtree", interface_filter)
    )

    root = parse_netconf_xml(reply.xml)

    return validate_oper_status(
        root,
        interface_name
    )

def validate_iosxe_oper_status(root, interface_name):
    namespace = {
        "iosxe": (
            "http://cisco.com/ns/yang/"
            "Cisco-IOS-XE-interfaces-oper"
        )
    }

    interfaces = root.findall(
        ".//iosxe:interface",
        namespace
    )

    for interface in interfaces:
        name_element = interface.find(
            "iosxe:name",
            namespace
        )

        if name_element is None:
            raise ValueError(
                "IOS XE NETCONF validation failed - "
                "missing interface name"
            )

        if name_element.text == interface_name:
            status_element = interface.find(
                "iosxe:oper-status",
                namespace
            )

            if status_element is None:
                raise ValueError(
                    "IOS XE NETCONF validation failed - "
                    f"missing oper-status for {interface_name}"
                )

            if status_element.text == "if-oper-state-ready":
                return True, "operational status is up"

            return False, (
                f"operational status is "
                f"{status_element.text}"
            )

    return False, f"interface {interface_name} not found"

def retrieve_and_validate_iosxe_interface(
    connection,
    interface_name
):
    oper_filter = f"""
    <interfaces xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-interfaces-oper">
        <interface>
            <name>{interface_name}</name>
        </interface>
    </interfaces>
    """

    reply = connection.get(
        filter=("subtree", oper_filter)
    )

    root = parse_netconf_xml(reply.xml)

    return validate_iosxe_oper_status(
        root,
        interface_name
    )
