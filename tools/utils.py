import sys
from pathlib import Path

from processing.directory import Directory, EmptyDirectory


def print_error(*values, sep=' ', end='\n', file=None) -> None:
    print("ERROR:", *values, sep=sep, end=end, file=file)


def get_directory(args: dict, key: str) -> Directory:
    if args[key] is None:
        return EmptyDirectory()

    directory = Directory(Path(args[key]))

    if directory:
        if not directory.path.is_dir():
            print_error("data directory was not found:", directory)
            sys.exit(1)

    return directory
