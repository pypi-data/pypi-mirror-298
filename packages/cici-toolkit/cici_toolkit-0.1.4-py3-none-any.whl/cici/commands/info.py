#!/usr/bin/env python3

import argparse
import logging
from typing import Any

from cici.binary import Binary
from cici.util import capture_warnings

from ._common import add_common_arguments, open_file


_LOG = logging.getLogger(__name__)


_STRICT_MSG = """
This may be due to a poorly authored or edited file, or it might be due to corruption.
In some cases, it might be that this tool needs to be updated to support this file.
Please send this file to nago for analysis!
"""

# info [--strict] [--debug] [--e/emotions] [--i/images] [-v/--verbose] file[s]...

# --show-warnings: on by default
# add a -Werror flag to treat warnings as errors for sake of return code; implies show-warnings
# make --strict imply -Werror


def info(
    filename: str,
    strict: bool,
    show_warnings: bool,
    show_emotions: bool = False,
    show_images: bool = False,
) -> None:

    def _print_summary_table(avb: Binary) -> None:
        print("")
        print("Summary")
        print("=======")
        print("")
        avb.print_summary(advanced=False)
        print("")

    def _print_emotion_table(avb: Binary) -> None:
        if show_emotions:
            print("")
            print("Emotion Table")
            print("=============")
            # emotion table will insert blank lines before each section, so skip it here.
            avb.print_emotion_table()
            print("")

    def _print_image_table(avb: Binary) -> None:
        if show_images:
            print("")
            print("Image Table")
            print("===========")
            print("")
            avb.print_image_table()
            print("")

    def _info(avb: Binary) -> None:

        _print_summary_table(avb)
        _print_emotion_table(avb)
        try:
            avb.read_images(evaluate=True)
        except ExceptionGroup as exc_group:
            if show_images:
                # The image table will show all of these errors in a
                # suitable way for human consumption, avoid re-raising
                # them to be handled in the general case. Do, however,
                # log the exception info to the debugging stream.
                for exc in exc_group.exceptions:  # pylint: disable=not-an-iterable
                    _LOG.debug("Muffled error from read_images():", exc_info=exc)
                msg = f"There were {len(exc_group.exceptions)} problems parsing images."
                # debug handler will show full gore in the stack trace,
                # but full gore is already logged, so skip it.
                # in non-debug mode, we don't want the gore anyway.
                raise SystemExit(msg) from None
            raise
        finally:
            # read_images() may raise an Exception (or group), but we
            # still want to print the image table if we succeeded in
            # making one, which will contain error summaries based on
            # those exceptions in its output.
            _print_image_table(avb)

        if strict:
            try:
                avb.strictness_check()
                print("\nStrictness check: ✅")
            except Exception:
                print("\nStrictness check: ❌")
                print(_STRICT_MSG)
                raise

    with capture_warnings("cici") as warnings:
        with open_file(filename, parse_images=False, autorepair=False) as avb:
            try:
                _info(avb)
            finally:
                if show_warnings and warnings:
                    print("Warnings:")
                    for msg in warnings:
                        print(f"  - {msg}")
                    print("")


def register(subparsers: Any) -> None:
    subparser = subparsers.add_parser("info", help="Show information about AVB/BGB files")

    subparser.add_argument(
        "-e",
        "--emotions",
        action="store_true",
        help="Show pose/emotion/gesture information",
    )

    subparser.add_argument(
        "-i",
        "--images",
        action="store_true",
        help="Show image table information",
    )

    subparser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Verbose output: show emotion and image tables (implies -e, -i)",
    )

    subparser.add_argument(
        "-s",
        "--strict",
        action="store_true",
        help="Show pedantic warnings.",
    )

    subparser.add_argument(
        "--hide-warnings",
        action="store_true",
        help="Don't show warnings for non-fatal problems with the file.",
    )
    add_common_arguments(subparser)
    subparser.add_argument("filename")


def dispatch(args: argparse.Namespace) -> None:
    info(
        args.filename,
        args.strict,
        not args.hide_warnings,
        show_emotions=args.emotions or args.verbose,
        show_images=args.images or args.verbose,
    )
