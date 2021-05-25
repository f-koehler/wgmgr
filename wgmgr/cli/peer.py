from __future__ import annotations

from ipaddress import IPv4Address, IPv6Address
from pathlib import Path

from typer import Argument, Typer, echo

from wgmgr.cli import common
from wgmgr.config.main import MainConfig
from wgmgr.error import DuplicatePeerError

app = Typer()


@app.command()
def add(
    name: str = Argument(..., help="Name of the peer."),
    config_path: Path = common.OPTION_CONFIG_PATH,
    port: int | None = common.OPTION_PORT,
    ipv4_address: str | None = common.OPTION_IPV4_ADDRESS,
    ipv6_address: str | None = common.OPTION_IPV6_ADDRESS,
):
    config = MainConfig.load(config_path)
    try:
        config.add_peer(
            name,
            IPv4Address(ipv4_address) if ipv4_address else None,
            IPv6Address(ipv6_address) if ipv6_address else None,
            port,
        )
    except DuplicatePeerError as e:
        echo(str(e), err=True)
    config.save(config_path)


# @app.command()
# def remove(
#     name: str = Argument(..., help="Name of the peer."),
#     config_path: Path = common.OPTION_CONFIG_PATH,
# ):
#     pass
