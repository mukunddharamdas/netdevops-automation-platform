
import argparse
import yaml

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from config_validation import validate_ip_address


def generate_configuration(data):
    # Validate all interfaces before rendering
    for interface in data["interfaces"]:
        ip_address = interface["ip_address"]

        if not validate_ip_address(ip_address):
            raise ValueError(
                f"Invalid IP address {ip_address} "
                f"for interface {interface['name']}"
            )

    # Load the Jinja2 template
    environment = Environment(
        loader=FileSystemLoader("templates"),
        trim_blocks=True,
        lstrip_blocks=True,
        undefined=StrictUndefined
    )

    template = environment.get_template("interface_config.j2")

    # Return the generated configuration
    return template.render(interfaces=data["interfaces"])


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Generate validated network configuration"
    )

    parser.add_argument(
        "--show-config",
        action="store_true",
        help="Display the generated configuration"
    )

    args = parser.parse_args()

    try:
        with open("config_data.yaml", "r") as file:
            data = yaml.safe_load(file)

        rendered_config = generate_configuration(data)

        print("Configuration generated successfully")
        print(f"Configuration size: {len(rendered_config)} characters")

        if args.show_config:
            print("\n===== GENERATED CONFIGURATION =====")
            print(rendered_config)

    except Exception as error:
        print(
            f"ERROR - Configuration generation failed: "
            f"{type(error).__name__}"
        )
        raise SystemExit(1)

    raise SystemExit(0)
