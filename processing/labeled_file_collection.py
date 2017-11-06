from pathlib import Path

from collections import defaultdict

from processing.file_collection import FileCollection


class LabeledFileCollection(FileCollection):
    """
    This is a file collection that associates each file with a label. It
    provides methods to access the files using the corresponding label.
    """

    def __init__(self):
        self._files = defaultdict(list)

    def add(self, file: Path, label):
        """ Adds a new file to the collection with the specified label """
        self._files[label].append(file)

    def __iter__(self):
        def iterator(files: dict):
            for file_list in files.values():
                for file in file_list:
                    yield file

        return iterator(self._files)

    def __getitem__(self, label):
        """ Returns a list of files with the specified label """
        return self._files[label]

    def labels(self):
        """ Returns list with the labels available """
        return list(self._files.keys())

    def iter_by_label(self):
        """
        Returns iterator that iterates over each file and its corresponding
        label.
        """

        def iterator(files: dict):
            """ Yields each file and its corresponding label """
            for label, file_list in files.items():
                for file in file_list:
                    yield file, label

        return iterator(self._files)
