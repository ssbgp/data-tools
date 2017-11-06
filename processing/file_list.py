from collections import Iterable

from processing.file_collection import FileCollection


class FileList(FileCollection):
    """ A simple list of files """

    def __init__(self, iterable: Iterable):
        self._list = list(iterable)

    def __iter__(self):
        return iter(self._list)
