import logging

import structlog
from rich.console import Console
from rich.logging import RichHandler
from typer import Typer

from src.logging_conf import setup_logging
from src.process.processor import Processor
from src.settings import config

app = Typer(help="CLI - CLI Description")
console = Console()


@app.command()
def process():
    root_logger = structlog.get_logger("src")
    for handler in root_logger.handlers:
        if isinstance(handler, RichHandler):
            handler.console = console
            handler.show_time = False
            handler.show_path = False
            handler.setLevel(logging.WARNING)

    processor = Processor()
    processor.process()


def main() -> None:
    setup_logging()
    app()


if __name__ == "__main__":
    main()
