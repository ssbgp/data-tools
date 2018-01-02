from pathlib import Path
from typing import Iterator, cast

from processing.file_container import FileContainer


class Directory(FileContainer):
    """ File container based on a single directory. """

    def __init__(self, directory: Path) -> None:
        self._path = directory

    def __iter__(self) -> Iterator[Path]:
        return iter(self._path.iterdir())

    def glob(self, pattern: str) -> Iterator[Path]:
        return iter(self._path.glob(pattern))

    def __eq__(self, other: object) -> bool:
        other = cast(Directory, other)
        return self._path == other._path

    def __hash__(self) -> int:
        return hash(self._path)

    @property
    def path(self) -> Path:
        return self._path

    def __str__(self) -> str:
        return str(self._path)

    def __repr__(self) -> str:
        return repr(self._path)


class EmptyDirectory(Directory):
    """ An empty directory is an abstraction of a directory with no files """

    def __init__(self) -> None:
        super().__init__(Path(""))

    def __iter__(self) -> Iterator[Path]:
        return iter([])

    def glob(self, pattern: str) -> Iterator[Path]:
        return iter([])
