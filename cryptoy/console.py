import click
import logging

from rich.logging import RichHandler
from rich.console import Console

from . import __version__


logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)
console = Console()


@click.command()
@click.version_option(version=__version__)
def main():
    log = logging.getLogger("console")

    log.info("Hello world!")
