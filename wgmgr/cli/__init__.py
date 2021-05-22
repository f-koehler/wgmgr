import logging

from typer import Typer

from wgmgr.cli import config, peer

logging.basicConfig(level=logging.INFO)

app = Typer()
app.add_typer(config.app, name="config", help="Manage a config file.")
app.add_typer(peer.app, name="peer", help="Manage peers.")

if __name__ == "__main__":
    app()
