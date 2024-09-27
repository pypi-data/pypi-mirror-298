import argparse
import shlex
import sys


__version__ = "1.3.0"


def quote(skip_empty: bool, newline: bool, keep_trailing_newline: bool) -> None:
    # Read in stdin
    data: str = "".join(line for line in sys.stdin)
    if not data:
        return
    if not keep_trailing_newline and data.endswith("\n"):
        data = data[:-1]
    # Quote lines
    items: list[str] = data.split("\n")
    if skip_empty:
        items = [i for i in items if len(i) > 0]
    quoted: list[str] = [shlex.quote(i) for i in items]
    # Output
    output: str = ("\n" if newline else " ").join(quoted)
    print(output, flush=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action="version", version=f"{parser.prog} {__version__}")
    parser.add_argument(
        "-n", "--newline", action="store_true", help="Output arguments with newline instead of a space as a delimiter"
    )
    parser.add_argument("-s", "--skip-empty", action="store_true", help="Do not output empty quoted strings")
    parser.add_argument(
        "-k", "--keep_newline", action="store_true", help="Do not ignore the final character if it is a newline"
    )
    return parser.parse_args()


def cli():
    quote(**vars(parse_args()))
