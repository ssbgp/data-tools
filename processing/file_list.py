from pathlib import Path
from typing import Iterator

from collections import Iterable

from processing.file_collection import FileCollection


class FileList(FileCollection):
    """ A simple list of files """

    def __init__(self, iterable: Iterable) -> None:
        self._list = list(iterable)

    def __iter__(self) -> Iterator[Path]:
        """ Returns an iterator to iterate over each file in the list """
        return iter(self._list)
