import argparse
import sys

from termcolor import colored

from ._version import __version__


def _legend() -> str:
    legend = (
        "Digit:     " + colored("RED", "red"),
        "Special:   " + colored("BLUE", "blue"),
        "Uppercase: " + colored("GREEN", "green"),
        "Lowercase: " + colored("DEFAULT", None),
    )
    return "Legend:\n  " + "\n  ".join(legend)


def _color_char(c: str) -> str:
    if c.islower():
        return c
    if c.isupper():
        return colored(c, "green")
    if c.isdigit():
        return colored(c, "red")
    return colored(c, "blue")


def _print_colored(s: str) -> None:
    print("".join(_color_char(i) for i in s), end="", flush=True)


def _main(string: str | None, legend: bool) -> None:
    printed = True
    if string == "-":
        for block in sys.stdin:
            _print_colored(block)
    elif string is not None:
        _print_colored(string)
        print()
    else:
        printed = False
    if legend:
        print(("\n" if printed else "") + _legend(), end="")
    elif not printed:
        print("Error: No arguments passed.", file=sys.stderr)
        sys.exit(1)


def cli() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "string", nargs="?", default=None, help="The string to print clearly. Read from stdin if string is: -"
    )
    parser.add_argument("--legend", action="store_true", help="Print the color code legend at the end.")
    parser.add_argument("--version", action="version", version=f"{parser.prog} {__version__}")
    _main(**vars(parser.parse_args()))
