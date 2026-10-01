import pytest

from netconf_validation import (
    parse_netconf_xml,
    validate_oper_status,
    validate_iosxe_oper_status,
)

def test_valid_netconf_xml():

    xml_data = """
    <interface>
        <name>Vlan20</name>
        <oper-status>down</oper-status>
    </interface>
    """

    root = parse_netconf_xml(xml_data)

    assert root.tag == "interface"

def test_invalid_netconf_xml():

    xml_data = """
    <interface>
        <name>Vlan20</name>
        <oper-status>down</oper-status>
    """

    with pytest.raises(
        ValueError,
        match="Invalid NETCONF XML"
    ):
        parse_netconf_xml(xml_data)

def test_oper_status_up():

    xml_data = """
    <interfaces>
        <interface>
            <name>Vlan20</name>
            <oper-status>up</oper-status>
        </interface>
    </interfaces>
    """

    root = parse_netconf_xml(xml_data)

    result, reason = validate_oper_status(root, "Vlan20")

    assert result is True
    assert reason == "operational status is up"


def test_oper_status_down():

    xml_data = """
    <interfaces>
        <interface>
            <name>Vlan20</name>
            <oper-status>down</oper-status>
        </interface>
    </interfaces>
    """

    root = parse_netconf_xml(xml_data)

    result, reason = validate_oper_status(root, "Vlan20")

    assert result is False
    assert reason == "operational status is down"

def test_interface_not_found_netconf():

    xml_data = """
    <interfaces>
        <interface>
            <name>Vlan10</name>
            <oper-status>up</oper-status>
        </interface>
    </interfaces>
    """
    root = parse_netconf_xml(xml_data)

    result, reason = validate_oper_status(root, "Vlan20")

    assert result is False
    assert reason == "interface Vlan20 not found"

def test_oper_status_with_namespace():

    xml_data = """
    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
            <name>Vlan20</name>
            <oper-status>up</oper-status>
        </interface>
    </interfaces>
    """

    root = parse_netconf_xml(xml_data)

    result, reason = validate_oper_status(root, "Vlan20")

    assert result is True
    assert reason == "operational status is up"

def test_missing_oper_status_raises_error():

    xml_data = """
    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
            <name>Vlan20</name>
        </interface>
    </interfaces>
    """

    root = parse_netconf_xml(xml_data)

    with pytest.raises(
        ValueError,
        match="missing oper-status for Vlan20"
    ):
        validate_oper_status(root, "Vlan20")

def test_realistic_netconf_rpc_reply():

    xml_data = """
    <rpc-reply
        xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"
        message-id="101">

        <data>
            <interfaces
                xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">

                <interface>
                    <name>Vlan10</name>
                    <oper-status>up</oper-status>
                </interface>

                <interface>
                    <name>Vlan20</name>
                    <oper-status>down</oper-status>
                </interface>

            </interfaces>
        </data>
    </rpc-reply>
    """

    root = parse_netconf_xml(xml_data)

    result, reason = validate_oper_status(
        root,
        "Vlan20"
    )

    assert result is False
    assert reason == "operational status is down"

def test_iosxe_oper_status_ready():
    xml_data = """
    <rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <data>
            <interfaces xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-interfaces-oper">
                <interface>
                    <name>GigabitEthernet1</name>
                    <admin-status>if-state-up</admin-status>
                    <oper-status>if-oper-state-ready</oper-status>
                </interface>
            </interfaces>
        </data>
    </rpc-reply>
    """

    root = parse_netconf_xml(xml_data)

    result, reason = validate_iosxe_oper_status(
        root,
        "GigabitEthernet1"
    )

    assert result is True
    assert reason == "operational status is up"

def test_iosxe_oper_status_not_ready():
    xml_data = """
    <rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <data>
            <interfaces xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-interfaces-oper">
                <interface>
                    <name>GigabitEthernet2</name>
                    <admin-status>if-state-up</admin-status>
                    <oper-status>if-oper-state-no-pass</oper-status>
                </interface>
            </interfaces>
        </data>
    </rpc-reply>
    """

    root = parse_netconf_xml(xml_data)

    result, reason = validate_iosxe_oper_status(
        root,
        "GigabitEthernet2"
    )

    assert result is False
    assert reason == "operational status is if-oper-state-no-pass"
    