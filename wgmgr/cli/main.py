from typer import Typer

from .config import app as app_config

app = Typer()
app.add_typer(app_config, name="config")

if __name__ == "__main__":
    app()
