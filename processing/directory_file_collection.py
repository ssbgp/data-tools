from pathlib import Path

from processing.file_collection import FileCollection


class DirectoryFileCollection(FileCollection):
    """
    File collection to abstract a directory. It obtains its files from an
    existing directory.
    """

    def __init__(self, directory: Path):
        self.directory = directory

    def __iter__(self):
        return self.directory.iterdir()

    def glob(self, pattern: str):
        return self.directory.glob(pattern)
