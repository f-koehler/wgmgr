import logging

from typer import Typer

from wgmgr.cli import config, p2p, peer

logging.basicConfig(level=logging.INFO)

app = Typer()
app.add_typer(config.app, name="config", help="Manage a config file.")
app.add_typer(peer.app, name="peer", help="Manage peers.")
app.add_typer(
    p2p.app, name="p2p", help="Manage point-to-point connections between peers."
)

if __name__ == "__main__":
    app()
