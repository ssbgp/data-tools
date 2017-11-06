from abc import abstractmethod
from collections import Iterable


class FileCollection(Iterable):
    """
    Abstraction of a data structure to hold multiple files (paths to files).
    """

    @abstractmethod
    def __iter__(self):
        """ Returns an iterator to iterate over each file in the collection """
