from pathlib import Path
from collections import Iterable

from processing.file_collection import FileCollection


class MultiDirectoryFileCollection(FileCollection):
    """
    File collection to abstract a directory. It obtains its files from an
    existing directory.
    """

    def __init__(self, *directories: Path):
        self.directories = directories

    def __iter__(self):
        def iterator(directories: Iterable):
            for directory in self.directories:
                for file in directory.iterdir():
                    yield file

        return iterator(self.directories)

    def glob(self, pattern: str):
        for directory in self.directories:
            for file in directory.glob(pattern):
                yield file
