from typer import Typer

from .config import app as app_config
from .connection import app as app_connection
from .peer import app as app_peer

app = Typer()
app.add_typer(app_config, name="config")
app.add_typer(app_peer, name="peer")
app.add_typer(app_connection, name="connection")

if __name__ == "__main__":
    app()
