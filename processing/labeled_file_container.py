from pathlib import Path
from typing import Dict, Iterator, Tuple

from processing.directory import Directory
from processing.file_container import FileContainer
from processing.types import Label


class LabeledFileContainer(FileContainer):
    """
    This is a file container that aggregates multiple containers, associating each container with
    a label. It provides methods to access each container by its label.
    """

    def __init__(self, containers: Dict[Label, FileContainer]) -> None:
        self._containers: Dict[Label, FileContainer] = containers

    def __iter__(self) -> Iterator[Path]:
        """ Returns iterator to iterate over each file in this container """

        def iterator() -> Iterator[Path]:
            for container in self._containers.values():
                for file in container:
                    yield file

        return iterator()

    def iter_by_label(self) -> Iterator[Tuple[Label, Path]]:
        """ Returns iterator to iterate over each file and its corresponding label """

        def iterator() -> Iterator[Tuple[Label, Path]]:
            for label, container in self._containers.items():
                for file in container:
                    yield label, file

        return iterator()

    def glob(self, pattern: str) -> Iterator[Path]:
        """ Returns iterator to iterate over each file matching the given *pattern* """

        def iterator() -> Iterator[Path]:
            for container in self._containers.values():
                for file in container.glob(pattern):
                    yield file

        return iterator()

    def glob_by_label(self, pattern: str) -> Iterator[Tuple[Label, Path]]:
        """
        Returns iterator to iterate over each file matching the given *pattern* and its
        corresponding label
        """

        def iterator() -> Iterator[Tuple[Label, Path]]:
            for label, container in self._containers.items():
                for file in container.glob(pattern):
                    yield label, file

        return iterator()

    def __str__(self) -> str:
        return str(self._containers)

    def __repr__(self) -> str:
        return repr(self._containers)
