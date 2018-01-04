import csv
from pathlib import Path
from typing import Any, Dict, List


class CSVPrinter:

    def __init__(self, path: Path):
        self._path = path
        self._file = None
        self._writer: csv.DictWriter = None

    def __enter__(self):
        self._file = open(self._path, 'w', newline='').__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._file.__exit__(exc_type, exc_val, exc_tb)

    def set_headers(self, headers: List[str]):
        self._writer = csv.DictWriter(self._file, fieldnames=headers)
        self._writer.writeheader()

    def print_row(self, row: Dict[str, Any]):

        try:
            self._writer.writerow(row)
        except AttributeError:
            # set_headers() was not called before printing a row
            raise ValueError("CSVPrinter: cannot write a row before the headers having been set")


