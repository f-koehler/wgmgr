from typer import Typer

from .config import app as app_config
from .peer import app as app_peer

app = Typer()
app.add_typer(app_config, name="config")
app.add_typer(app_peer, name="peer")

if __name__ == "__main__":
    app()
