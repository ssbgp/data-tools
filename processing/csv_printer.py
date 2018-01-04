import csv
from pathlib import Path
from typing import Any, Dict


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

    def print_row(self, row: Dict[str, Any]):
        if not self._writer:
            self._writer = csv.DictWriter(self._file, fieldnames=list(row.keys()))
            self._writer.writeheader()

        self._writer.writerow(row)
