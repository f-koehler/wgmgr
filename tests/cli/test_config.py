import tempfile

from typer.testing import CliRunner

from wgmgr.cli.config import app


runner = CliRunner()


def test_ansible_group():
    with tempfile.TemporaryFile() as tmp:
        result = runner.invoke(
            app,
            ["new", "--backend", "ansible_group", "--backend-option", f"path:{tmp}"],
        )
        assert result.exit_code == 0

        result = runner.invoke(
            app,
            [
                "set",
                "default-port",
                "--backend",
                "ansible_group",
                "--backend-option",
                f"path:{tmp}",
                4242,
            ],
        )
        assert result.exit_code == 0
