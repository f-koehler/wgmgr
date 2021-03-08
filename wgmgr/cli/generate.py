import shutil
import subprocess
from pathlib import Path
from typing import Optional

from typer import Argument, Option, Typer

from wgmgr.cli import common
from wgmgr.config import Config
from wgmgr.templates import load_template

app = Typer()


@app.command()
def wg_quick(
    path: Path = common.config_file,
    output: Optional[Path] = Option(
        None, "-o", "--output", help="path for the wg-quick config file"
    ),
    force: bool = Option(
        False,
        "-f",
        "--force",
        help="whether to overwrite existing wg-quick config file",
    ),
    peer: str = Argument(..., help="peer to generate config for"),
):
    config = Config.load(path)

    if config.get_peer(peer) is None:
        raise RuntimeError(f'no peer named "{peer}"')

    template = load_template("wg-quick.conf.j2")
    generated = template.render(peer_name=peer, config=config)

    if output is None:
        print(generated)
        return

    if output.exists() and not force:
        raise RuntimeError(
            f'config file "{output}" exists, ' "use -f/--force to overwrite"
        )

    with open(output, "w") as fptr:
        fptr.write(generated)


@app.command()
def qr_code(
    path: Path = common.config_file,
    output: Optional[Path] = Option(
        None, "-o", "--output", help="path for the QR code image file"
    ),
    force: bool = Option(
        False, "-f", "--force", help="whether to overwrite existing QR code image file"
    ),
    peer: str = Argument(..., help="peer to generate QR code for"),
):
    config = Config.load(path)

    if config.get_peer(peer) is None:
        raise RuntimeError(f'no peer named "{peer}"')

    qrencode = shutil.which("qrencode")
    if not qrencode:
        raise RuntimeError("cannot find qrencode")

    template = load_template("wg-quick.conf.j2")
    generated = template.render(peer_name=peer, config=config)

    if output is None:
        subprocess.run([qrencode, "-t", "ansiutf8", generated])
        return

    if output.exists() and not force:
        raise RuntimeError(
            f'QR code file "{output}" exists, ' "use -f/--force to overwrite"
        )

    subprocess.run([qrencode, generated, "-o", output])
