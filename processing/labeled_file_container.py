from pathlib import Path
from typing import Dict, Iterator, Tuple

from processing.directory import Directory
from processing.file_container import FileContainer
from processing.types import Label


class LabeledFileContainer(FileContainer):
    """
    This is a file container that associates each file with a label. It
    provides methods to access the files using the corresponding label.
    """

    def __init__(self, directories: Dict[Label, Directory]) -> None:
        self._directories: Dict[Label, Directory] = directories

    def __iter__(self) -> Iterator[Path]:
        """ Returns iterator to iterate over each file in this container """

        def iterator() -> Iterator[Path]:
            for directory in self._directories.values():
                for file in directory:
                    yield file

        return iterator()

    def iter_by_label(self) -> Iterator[Tuple[Label, Path]]:
        """ Returns iterator to iterate over each file and its corresponding label """

        def iterator() -> Iterator[Tuple[Label, Path]]:
            for label, directory in self._directories.items():
                for file in directory:
                    yield label, file

        return iterator()

    def glob(self, pattern: str) -> Iterator[Path]:
        """ Returns iterator to iterate over each file matching the given *pattern* """

        def iterator() -> Iterator[Path]:
            for directory in self._directories.values():
                for file in directory.glob(pattern):
                    yield file

        return iterator()

    def glob_by_label(self, pattern: str) -> Iterator[Tuple[Label, Path]]:
        """
        Returns iterator to iterate over each file matching the given *pattern* and its
        corresponding label
        """

        def iterator() -> Iterator[Tuple[Label, Path]]:
            for label, directory in self._directories.items():
                for file in directory.glob(pattern):
                    yield label, file

        return iterator()

    def __str__(self) -> str:
        return str(self._directories)

    def __repr__(self) -> str:
        return repr(self._directories)
