from pathlib import Path
from ipaddress import IPv4Network, IPv6Network
from typing import Optional, List

from typer import Typer, Argument, Option

from wgmgr.backends import Backends, create_backend
from wgmgr.config import Config

app = Typer()
app_set = Typer()
app.add_typer(app_set, name="set")


@app.command()
def new(
    backend: Backends = Option(
        ...,
        help="configuration backend to use",
    ),
    backend_option: Optional[List[str]] = Option(
        None, help="options for the configuration backend"
    ),
    ipv4_subnet: Optional[str] = Option(None, "-4", "--ipv4", help="IPv4 subnet"),
    ipv6_subnet: Optional[str] = Option(None, "-6", "--ipv6", help="IPv6 subnet"),
    port: int = Option(51902, "-p", "--port", help="default port for new peers"),
):
    """Create a new, empty config."""

    config = Config(
        IPv4Network(ipv4_subnet) if ipv4_subnet else None,
        IPv6Network(ipv6_subnet) if ipv6_subnet else None,
        port,
    )
    backend = create_backend(backend, backend_option)
    backend.save(config)


@app_set.command()
def default_port(
    backend: Backends = Option(
        ...,
        help="configuration backend to use",
    ),
    backend_option: Optional[List[str]] = Option(
        None, help="options for the configuration backend"
    ),
    port: int = Argument(..., help="default port for new peers"),
):
    """Set default port."""
    backend = create_backend(backend, backend_option)
    config = backend.load()
    config.default_port = port
    backend.save(config)


@app_set.command()
def ipv4(
    backend: Backends = Option(
        ...,
        help="configuration backend to use",
    ),
    backend_option: Optional[List[str]] = Option(
        None, help="options for the configuration backend"
    ),
    ipv4_subnet: str = Argument(..., help="IPv4 subnet"),
):
    """Set default IPv4 subnet."""
    subnet = IPv4Network(ipv4_subnet)


if __name__ == "__main__":
    app()