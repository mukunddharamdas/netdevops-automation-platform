from unittest.mock import Mock

from netconf_validation import (
    parse_netconf_xml,
    validate_oper_status,
    retrieve_and_validate_interface
)

def test_mock_reply():
    fake_reply = Mock()

    fake_reply.xml = """
    <interface>
        <name>Vlan20</name>
        <oper-status>down</oper-status>
    </interface>
    """

    assert "Vlan20" in fake_reply.xml

def test_mock_reply_validation():
    fake_reply = Mock()

    fake_reply.xml = """
    <rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <data>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface>
                    <name>Vlan20</name>
                    <oper-status>down</oper-status>
                </interface>
            </interfaces>
        </data>
    </rpc-reply>
    """

    root = parse_netconf_xml(fake_reply.xml)

    result, reason = validate_oper_status(
        root,
        "Vlan20"
    )

    assert result is False
    assert reason == "operational status is down"


def test_mock_connection_get():
    fake_connection = Mock()
    fake_reply = Mock()

    fake_reply.xml = """
    <rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <data>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface>
                    <name>Vlan20</name>
                    <oper-status>up</oper-status>
                </interface>
            </interfaces>
        </data>
    </rpc-reply>
    """

    fake_connection.get.return_value = fake_reply

    reply = fake_connection.get(
        filter=("subtree", "<interfaces></interfaces>")
    )

    root = parse_netconf_xml(reply.xml)

    result, reason = validate_oper_status(
        root,
        "Vlan20"
    )

    assert result is True
    assert reason == "operational status is up"

def test_retrieve_and_validate_interface():
    fake_connection = Mock()
    fake_reply = Mock()

    fake_reply.xml = """
    <rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <data>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface>
                    <name>Vlan20</name>
                    <oper-status>up</oper-status>
                </interface>
            </interfaces>
        </data>
    </rpc-reply>
    """

    fake_connection.get.return_value = fake_reply

    result, reason = retrieve_and_validate_interface(
        fake_connection,
        "Vlan20"
    )

    assert result is True
    assert reason == "operational status is up"