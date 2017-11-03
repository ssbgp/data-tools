from abc import abstractmethod
from collections import Iterable


class FileCollection(Iterable):
    """ Abstraction to hold multiple files """

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def glob(self, pattern: str):
        """
        Iterate over the files and yield all existing files (of any kind,
        including directories) matching the given pattern.

        :param pattern: pattern to match files to
        """
        pass
