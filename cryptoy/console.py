"""console interface for cryptoy."""

import logging

import click
from rich.console import Console
from rich.logging import RichHandler

from . import __version__

console = Console()
logger = logging.getLogger(__name__)


def setup_logging():
    logging.basicConfig(
        level="INFO",
        format="%(name)s:%(funcName)s - %(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)],
    )

    logger.info("Hello world! (log)")
    console.log("Hello world (console)")


@click.group()
@click.version_option(version=__version__)
@click.option("--verbose", "-v", is_flag=True, help="Enables verbose mode.")
@click.pass_context
def cli(ctx, verbose):
    """CLI entrypoint for crypto.console."""
    pass


@cli.command()
def create_key():
    setup_logging()
