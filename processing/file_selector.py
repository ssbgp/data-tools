from abc import abstractmethod, ABC
from processing.file_collection import FileCollection


class FileSelector(ABC):
    """
    File selectors are responsible for selecting data files.
    The implementation specifies how and which files are selected.
    """

    @abstractmethod
    def select(self, files: FileCollection) -> list:
        """
        Selects specific data files from a file a collection.

        :param files: collection of file to select from
        :return: list containing a paths corresponding to selected data files
        """
