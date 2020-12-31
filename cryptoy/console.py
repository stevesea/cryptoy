"""console interface for cryptoy."""

from dataclasses import dataclass
import json
import logging

import click
from rich.console import Console
from rich.logging import RichHandler

from cryptoy.nacl.box import BoxKeyPair
from . import __version__

console = Console()
logger = logging.getLogger(__name__)


def setup_logging(verbosity: int):
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


@dataclass
class CTX:
    verbose: int = 0


@click.group()
@click.version_option(version=__version__)
@click.option("--verbose", "-v", count=True, help="Enables verbose mode.")
@click.pass_context
def cli(ctx, verbose):
    """CLI entrypoint for crypto.console."""
    ctx.ensure_object(CTX)
    ctx.obj.verbose = verbose
    setup_logging(verbose)
    logger.info("Hello world! (root)")


@cli.command("create-kp")
def pk_create():
    """Create a new Curve25519 keypair for public key encryption"""
    logger.info("Hello world! (pk)")
    console.log("Hello world (console)")

    kp = BoxKeyPair.generate()
    console.log(json.dumps(json.loads(kp.to_json()), indent=4))


@cli.command("box")
@click.option(
    "--sender-secret-key",
)
@click.option(
    "--receiver-public-key",
)
@click.argument("input", type=click.File("rb"))
@click.argument("output", type=click.File("wb"))
def pk_box():
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
def pk_unbox():
    """Decrypt a message from a sender to a receiver"""
    pass
