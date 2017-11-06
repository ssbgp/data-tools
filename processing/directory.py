from pathlib import Path

from processing.file_container import FileContainer


class Directory(FileContainer):
    """ File container based on a single directory. """

    def __init__(self, directory: Path):
        self._path = directory

    def __iter__(self):
        return self._path.iterdir()

    def glob(self, pattern: str):
        return self._path.glob(pattern)

    def __eq__(self, other):
        # noinspection PyProtectedMember
        return self._path == other._path

    def __hash__(self):
        return hash(self._path)

    @property
    def path(self) -> Path:
        return self._path

    def __str__(self) -> str:
        return str(self._path)

    def __repr__(self):
        return repr(self._path)


class EmptyDirectory(Directory):
    """ An empty directory is an abstraction of a directory with no files """

    def __init__(self):
        super().__init__(Path(""))

    def __iter__(self):
        return iter([])

    def glob(self, pattern: str):
        return iter([])
