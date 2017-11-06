from processing.file_selector import FileSelector
from processing.file_collection import FileCollection


class BasicFileSelector(FileSelector):
    """ Selects only .basic.csv files as data files """

    def select(self, files: FileCollection) -> list:
        return list(files.glob("*.basic.csv"))
