# tests/test_console.py
import click.testing
import pytest

from cryptoy.cli import nacl


@pytest.fixture
def runner():
    return click.testing.CliRunner()


def test_version(runner):
    result = runner.invoke(nacl.cli, ["--version"])
    assert result.exit_code == 0
