from __future__ import annotations

from pathlib import Path

from typer import Option

DEFAULT_CONFIG_PATH = Path("wgmgr.yml")

OPTION_CONFIG_PATH = Option(
    DEFAULT_CONFIG_PATH,
    "-c",
    "--config",
    envvar="WGMGR_CONFIG",
    help="Path of the config file.",
)

OPTION_PORT = Option(None, "-p", "--port", help="Port for WireGuard.")

OPTION_IPV4_NETWORK = Option(
    None,
    "-4",
    "--ipv4",
    help="IPv4 network in CIDR notation.",
)

OPTION_IPV6_NETWORK = Option(
    None,
    "-6",
    "--ipv6",
    help="IPv6 network in CIDR notation.",
)


OPTION_IPV4_ADDRESS = Option(
    None,
    "-4",
    "--ipv4",
    help="IPv4 address.",
)

OPTION_IPV6_ADDRESS = Option(
    None,
    "-6",
    "--ipv6",
    help="IPv6 address.",
)
