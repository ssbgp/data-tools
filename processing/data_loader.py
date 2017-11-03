from abc import abstractmethod, ABC


class DataLoader(ABC):
    """
    Data loaders are responsible for loading the data from the data files.
    The implementation specifies what data is collected and how is it stored
    in memory or other even on disk.
    """

    @abstractmethod
    def load(self, data_files: list):
        """
        Loads data from the specified data files. It returns a data structure
        holding the data. The type of structure returned is completely dependent
        on the implementation. The returned structure may have the data stored
        on disk and just provide an interface to access that data.

        :param data_files: list of data files to load data from
        :return: a data structure with the loaded data.
        """
