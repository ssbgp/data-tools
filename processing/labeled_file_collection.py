from pathlib import Path
from typing import Dict, List, Iterator, Tuple

from collections import defaultdict

from processing.file_collection import FileCollection
from processing.types import Label


class LabeledFileCollection(FileCollection):
    """
    This is a file collection that associates each file with a label. It
    provides methods to access the files using the corresponding label.
    """

    def __init__(self) -> None:
        self._files: Dict[Label, List[Path]] = defaultdict(list)

    def add(self, file: Path, label: Label) -> None:
        """ Adds a new file to the collection with the specified label """
        self._files[label].append(file)

    def __len__(self) -> int:
        """ Returns the number of files in the collection """
        count = 0
        for _, files in self._files.items():
            count += len(files)

        return count

    def __iter__(self) -> Iterator[Path]:
        """ Returns iterator to iterate over all files in the collection """

        def iterator() -> Iterator[Path]:
            for file_list in self._files.values():
                for file in file_list:
                    yield file

        return iterator()

    def __getitem__(self, label: Label) -> List[Path]:
        """ Returns a list of files with the specified label """
        return self._files[label]

    def labels(self) -> List[Label]:
        """ Returns list with all labels available """
        return list(self._files.keys())

    def iter_by_label(self) -> Iterator[Tuple[Label, Path]]:
        """ Returns iterator to iterate over all files and its corresponding label """

        def iterator() -> Iterator[Tuple[Label, Path]]:
            for label, file_list in self._files.items():
                for file in file_list:
                    yield label, file

        return iterator()
