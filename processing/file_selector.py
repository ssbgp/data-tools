from abc import abstractmethod, ABC
from processing.file_collection import FileCollection
from processing.file_container import FileContainer


class FileSelector(ABC):
    """
    File selectors are responsible for selecting data files.
    The implementation specifies how and which files are selected.
    """

    @abstractmethod
    def select(self, container: FileContainer) -> FileCollection:
        """
        Selects data files from a file container according to some criteria.
        Selected files are returned in a file collection.

        :param container: container of file to select from
        :return: file collection containing the selected files
        """
