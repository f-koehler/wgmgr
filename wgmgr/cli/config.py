from __future__ import annotations

from ipaddress import IPv4Network, IPv6Network
from pathlib import Path

from typer import Option, Typer, echo

from wgmgr.config.main import MainConfig

app = Typer()


DEFAULT_CONFIG_PATH = Path("/") / "etc" / "wgmgr.conf"


@app.command()
def new(
    config_path: Path = Option(
        DEFAULT_CONFIG_PATH, "-c", "--config", envvar="WGMGR_CONFIG"
    ),
    ipv4_network: str = Option("10.0.0.0/24", "-4", "--ipv4"),
    ipv6_network: str = Option("fd00:641:c767:bc00::/64", "-6", "--ipv6"),
    default_port: int = Option("51820", "-p", "--port"),
    force: bool = Option(False, "-f", "--force"),
):
    if config_path.exists() and (not force):
        echo(
            f'config file "{config_path}" exists, add -f/--force flag to overwrite',
            err=True,
        )
        exit(1)

    config = MainConfig(
        default_port, IPv4Network(ipv4_network), IPv6Network(ipv6_network)
    )
    config.save(config_path)
