from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network
from pathlib import Path
from typing import Any

import yaml
from typer import BadParameter


def load_yaml_file(path: Path) -> Any:
    with open(path) as fptr:
        return yaml.safe_load(fptr)


def generate_yaml(data: Any) -> str:
    try:
        from yaml import CDumper

        return yaml.dump(data, Dumper=CDumper)
    except ImportError:
        from yaml import Dumper

        return yaml.dump(data, Dumper=Dumper)


def write_yaml_file(path: Path, data: Any):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as fptr:
        fptr.write(generate_yaml(data))


def validate_subnet_ipv4(value: str) -> str:
    if value:
        IPv4Network(value)
    return value


def validate_address_ipv4(value: str) -> str:
    if value:
        IPv4Address(value)
    return value


def validate_subnet_ipv6(value: str) -> str:
    if value:
        IPv6Network(value)
    return value


def validate_address_ipv6(value: str) -> str:
    if value:
        IPv6Address(value)
    return value


def validate_port(value: int) -> int:
    if value and ((value < 0) or (value > 65535)):
        raise BadParameter(f"Invalid port number {value} (should be in range 0…65535)")
    return value
