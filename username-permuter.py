#!/usr/bin/env python3

from argparse import ArgumentParser
from pathlib import Path
from sys import exit
from typing import Set

MAX_FILESIZE = 1_000_000


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def error(message: str, exit_prog: bool = True):
    print(f"{Colors.FAIL}[-] {message}{Colors.ENDC}")
    if exit_prog:
        exit(1)


def get_lines_from_file(infile: Path) -> Set[str]:
    lines = set()
    with open(infile, mode="r", encoding="ascii") as handle:
        for line in handle.readlines():
            line = line.strip()
            if not line:
                continue

            if line.startswith("#"):
                continue

            lines.add(line.lower())

    return lines


def get_lowercase_permutations(list: Set[str]) -> Set[str]:
    result = set()
    for name in list:
        try:
            x, y = name.split()
            result.add(x)               # john
            result.add(y)               # doe
            result.add(f"{x[0]}.{y}")   # j.doe
            result.add(f"{x[0]}-{y}")   # j-doe
            result.add(f"{x[0]}_{y}")   # j_doe
            result.add(f"{x[0]}+{y}")   # j+doe
            result.add(f"{x[0]}{y}")    # jdoe
            result.add(f"{x}{y}")       # johndoe
            result.add(f"{y}{x}")       # doejohn
            result.add(f"{x}.{y}")      # john.doe
            result.add(f"{y}.{x}")      # doe.john
        except ValueError:
            result.add(name)

    return result


def get_uppercase_permutations(list: Set[str]) -> Set[str]:
    result = set()
    for name in list:
        try:
            x, y = name.split()
            result.add(x.capitalize())  # John
            result.add(y.capitalize())  # Doe
            result.add(x.upper())       # JOHN
            result.add(y.upper())       # DOE

            result.add(f"{x[0].upper()}.{y.capitalize()}")        # J.Doe
            result.add(f"{x[0].upper()}-{y.capitalize()}")        # J-Doe
            result.add(f"{x[0].upper()}_{y.capitalize()}")        # J_Doe
            result.add(f"{x[0].upper()}+{y.capitalize()}")        # J+Doe
            result.add(f"{x[0].upper()}{y.capitalize()}")         # JDoe
            result.add(f"{x.capitalize()}{y.capitalize()}")       # JohnDoe
            result.add(f"{y.capitalize()}{x.capitalize()}")       # DoeJohn
            result.add(f"{x.capitalize()}.{y.capitalize()}")      # John.Doe
            result.add(f"{y.capitalize()}.{x.capitalize()}")      # Doe.John

            result.add(f"{x[0].upper()}.{y.upper()}")   # J.DOE
            result.add(f"{x[0].upper()}-{y.upper()}")   # J-DOE
            result.add(f"{x[0].upper()}_{y.upper()}")   # J_DOE
            result.add(f"{x[0].upper()}+{y.upper()}")   # J+DOE
            result.add(f"{x[0].upper()}{y.upper()}")    # JDOE
            result.add(f"{x.upper()}{y.upper()}")       # JOHNDOE
            result.add(f"{y.upper()}{x.upper()}")       # DOEJOHN
            result.add(f"{x.upper()}.{y.upper()}")      # JOHN.DOE
            result.add(f"{y.upper()}.{x.upper()}")      # DOE.JOHN
        except ValueError:
            result.add(name.upper())

    return result


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="username-permuter",
        description="Calculates permutations of a userlist to check for e.g. using Kerbrute"
    )
    parser.add_argument(type=Path, dest="input", help="The input userlist to calculate permutations of")
    parser.add_argument(
        "-u", "--uppercase", dest="uppercase", action="store_true", help="Also generate uppercase permutations"
    )
    parser.add_argument(
        "-o", "--output", type=Path, dest="output", required=False, default=None,
        help="The output file do write the results to (prints to stdout if not specified)"
    )
    args = parser.parse_args()

    if not args.input.is_file():
        error("The input file does not exist")

    if args.output and args.output.is_file():
        error("The output file does already exist")

    if (size := args.input.stat().st_size) > MAX_FILESIZE:
        error(f"The file has {size} bytes, but max. {MAX_FILESIZE} bytes are allowed")

    initial = get_lines_from_file(args.input)
    values = get_lowercase_permutations(initial)
    if args.uppercase:
        uppercase = get_uppercase_permutations(initial)
        values = values.union(uppercase)

    values = sorted(values)
    if args.output:
        with open(args.output, mode="w", encoding="ascii") as outf:
            outf.writelines(list(map(lambda x: x + "\n", values)))
    else:
        for line in values:
            print(line)
