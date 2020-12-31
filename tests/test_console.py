# tests/test_console.py
import click.testing
import pytest

from cryptoy import console


@pytest.fixture
def runner():
    return click.testing.CliRunner()


def test_version(runner):
    result = runner.invoke(console.cli, ["--version"])
    assert result.exit_code == 0
