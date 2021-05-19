from typer import Typer

from wgmgr.cli import config

app = Typer()
app.add_typer(config.app, name="config", help="Manage config files.")

if __name__ == "__main__":
    app()
