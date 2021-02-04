import tempfile
from pathlib import Path

import pytest
from typer.testing import CliRunner

from wgmgr.cli.config import app

runner = CliRunner()


def test_config_new():
    # new config without any subnet should fail
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "config.yml"
        result = runner.invoke(
            app,
            ["new", "-c", path],
        )
        assert result.exit_code != 0

    # invalid IPv4 subnet should fail
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "config.yml"
        result = runner.invoke(app, ["new", "-c", path, "-4", "WW.XX.YY.ZZ"])
        assert result.exit_code != 0

    # valid IPv4 subnet should succeed
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "config.yml"
        result = runner.invoke(app, ["new", "-c", path, "-4", "10.0.0.0/24"])
        assert result.exit_code == 0


def test_config_set_default_port():
    # modifying non-existent config file should fail
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "config.yml"
        result = runner.invoke(
            app,
            ["set", "default-port", "-c", path, "1024"],
        )
        assert result.exit_code != 0

    # setting invalid ports should fail
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "config.yml"
        result = runner.invoke(
            app,
            ["new", "-c", path, "-4", "10.0.0.0/24"],
        )
        assert result.exit_code == 0

        result = runner.invoke(
            app,
            ["set", "default-port", "-c", path, "-1"],
        )
        assert result.exit_code != 0

        result = runner.invoke(
            app,
            ["set", "default-port", "-c", path, "90000"],
        )
        assert result.exit_code != 0
