from pathlib import Path

from processing.file_container import FileContainer


class Directory(FileContainer):
    """ File container based on a single directory. """

    def __init__(self, directory: Path):
        self.directory = directory

    def __iter__(self):
        return self.directory.iterdir()

    def glob(self, pattern: str):
        return self.directory.glob(pattern)

    @property
    def path(self) -> Path:
        return self.directory
