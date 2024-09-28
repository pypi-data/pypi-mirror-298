#!/usr/bin/env python3

import argparse
import logging
import sys

from . import commands
from .util import exc_summary, setup_logging


_LOG = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="cici",
        description="comic chat file toolkit",
        epilog="Made with love <3",
    )

    subparsers = parser.add_subparsers(
        title="Commands",
        dest="command",
        required=True,
        metavar="command",
        help="Description",
    )

    commands.info.register(subparsers)

    args = parser.parse_args()

    def _dispatch() -> None:
        setup_logging(args.debug)

        if args.command == "info":
            commands.info.dispatch(args)

    try:
        _dispatch()
    except KeyboardInterrupt:
        print("Interrupted via keyboard interrupt", file=sys.stderr)
        sys.exit(2)
    except (FileNotFoundError, PermissionError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(3)
    except ExceptionGroup as exc_group:
        print(f"{str(exc_group)}:", file=sys.stderr)
        for exc_ in exc_group.exceptions:  # pylint: disable=not-an-iterable
            print(f"  - {exc_summary(exc_)}", file=sys.stderr)
            for note in exc_.__notes__:
                print(f"    ({note})", file=sys.stderr)
            # If we just re-raise the exception, we may not see the
            # full traces if there are too many, so log them instead
            # so we can be assured to see them in debug mode.
            _LOG.debug(exc_, exc_info=exc_)
        sys.exit(4)
    except Exception as exc:  # pylint: disable=broad-exception-caught
        if args.debug:
            raise
        print(f"Exiting with error ({exc_summary(exc)})", file=sys.stderr)
        sys.exit(5)
    except SystemExit as exc:
        if isinstance(exc.code, str):
            print(f"Exiting with error: {str(exc)}", file=sys.stderr)
            sys.exit(6)
        raise


if __name__ == "__main__":
    main()

# check [--debug] file[s]...
#  - implies strict/validate
#  - quiet by default? (no summary, emotions or images table?)
#  - maybe add -e/-i as an option?
#  - maaaaybe add -summary as an option?
#  - -Werror would be good here.

# repair <infile> <outfile>

# extract [--raw] [--all-poses] <infile> <outdir>
