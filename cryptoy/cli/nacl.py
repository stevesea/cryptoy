"""console interface for cryptoy's NaCL commands."""

import json
import logging

import click
from rich.console import Console
from rich.logging import RichHandler

from cryptoy import __version__
from cryptoy.nacl.box import BoxKeyPair

console = Console()
logger = logging.getLogger(__name__)


def setup_logging(verbosity: int) -> None:
    levels = [
        logging.CRITICAL,
        logging.ERROR,
        logging.WARNING,
        logging.INFO,
        logging.DEBUG,
        logging.NOTSET,
    ]
    default_level = levels.index(logging.WARNING)

    logging.basicConfig(
        level=levels[min(len(levels) - 1, default_level + verbosity)],
        format="%(name)s:%(funcName)s - %(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)],
    )


@click.group()
@click.version_option(version=__version__)
@click.option("--verbose", "-v", count=True, help="Enables verbose mode.")
def cli(verbose: int) -> None:
    """CLI entrypoint for cryptoy-nacl."""
    setup_logging(verbose)
    logger.info("Hello world! (root)")


@cli.command("create-kp")
@click.argument("filename", type=click.File("w", encoding="UTF-8"))
def pk_create(filename) -> None:
    """Create a new Curve25519 keypair for public key encryption, write to FILENAME"""
    # logger.info("Hello world! (pk)")
    # console.log("Hello world (console)")

    kp = BoxKeyPair.generate()
    logger.debug(json.dumps(json.loads(kp.to_json()), indent=4))
    filename.write(kp.to_json())


@cli.command("box")
@click.option(
    "--sender-secret-key",
)
@click.option(
    "--receiver-public-key",
)
@click.argument("input", type=click.File("rb"))
@click.argument("output", type=click.File("wb"))
def pk_box() -> None:
    """Encrypt a message from a sender to a receiver"""
    pass


@cli.command("unbox")
@click.option(
    "--sender-public-key",
)
@click.option(
    "--receiver-secret-key",
)
@click.argument("input", type=click.File("rb"))
@click.argument("output", type=click.File("wb"))
def pk_unbox() -> None:
    """Decrypt a message from a sender to a receiver"""
    pass
