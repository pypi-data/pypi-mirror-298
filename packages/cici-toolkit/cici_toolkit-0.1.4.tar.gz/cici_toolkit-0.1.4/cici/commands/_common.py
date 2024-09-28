import argparse
from contextlib import contextmanager
import logging
import sys
from typing import Iterator

from cici.binary import Binary
from cici.util import exc_summary


def add_common_arguments(subparser: argparse.ArgumentParser) -> None:
    subparser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Show full debugging information and stack traces.",
    )


@contextmanager
def open_file(
    filename: str, parse_images: bool = True, autorepair: bool = False
) -> Iterator[Binary]:
    with open(filename, "rb") as file:
        try:
            avb = Binary(file, parse_images=False, autorepair=autorepair)
        except Exception as exc:  # pylint: disable=broad-exception-caught
            print(f"Unable to parse file: {exc_summary(exc)}", file=sys.stderr)
            logging.debug("Unable to parse file", exc_info=True)
            sys.exit(1)

        if parse_images:
            try:
                avb.read_images()
            except Exception as exc:  # pylint: disable=broad-exception-caught
                print(f"Unable to parse images: {exc_summary(exc)}", file=sys.stderr)
                logging.debug("Unable to parse images", exc_info=True)
                sys.exit(1)

        yield avb
