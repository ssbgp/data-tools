from processing.file_container import FileContainer
from processing.file_list import FileList
from processing.file_selector import FileSelector
from processing.file_collection import FileCollection
from processing.labeled_file_collection import LabeledFileCollection
from processing.labeled_file_container import LabeledFileContainer


class ExtensionFileSelector(FileSelector):
    """ Selects only files with the defined extension as data files """

    def __init__(self, extension: str):
        self.extension = extension
        self._pattern = f"*{self.extension}"

    def select(self, files: FileContainer) -> FileCollection:

        if isinstance(files, LabeledFileContainer):
            data_files = LabeledFileCollection()
            for file, label in files.glob_by_label(self._pattern):
                data_files.add(file, label)

            return data_files
        else:
            return FileList(files.glob(self._pattern))
