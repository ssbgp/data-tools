import csv
from contextlib import contextmanager
from os import PathLike


@contextmanager
def open_csv(path: PathLike):
    with open(path) as file:
        yield csv.DictReader(file, delimiter=";")
