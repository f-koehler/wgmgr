import pytest
from typer.testing import CliRunner

runner = CliRunner()


@pytest.fixture
def test_peer_new(tmpdir):
    print(tmpdir)
    assert False
