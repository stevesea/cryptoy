"""console interface for cryptoy."""

import logging

import click
from rich.console import Console
from rich.logging import RichHandler

from . import __version__

console = Console()
logger = logging.getLogger(__name__)


@click.command()
@click.version_option(version=__version__)
def main():
    """CLI entrypoint for crypto.console."""
    logging.basicConfig(
        level="INFO",
        format="%(name)s:%(funcName)s - %(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)],
    )

    logger.info("Hello world! (log)")
    console.log("Hello world (console)")
