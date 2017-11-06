from abc import ABC, abstractmethod


class FileContainer(ABC):
    """
    A file container is an abstraction for anything that can contain data
    files, such as, a directory or multiple directories.

    Accessing the file container may have some overhead. Usually, it implies
    accessing the disk or some remote server.
    """

    @abstractmethod
    def __iter__(self):
        """ Returns an iterator to iterate over each file in the container """

    @abstractmethod
    def glob(self, pattern: str):
        """
        Iterates over all files and yields all existing files (of any kind,
        including directories) matching the given pattern.

        :param pattern: pattern to match files to
        """
