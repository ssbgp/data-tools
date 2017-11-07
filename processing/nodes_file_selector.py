from processing.file_container import FileContainer
from processing.file_list import FileList
from processing.file_selector import FileSelector
from processing.file_collection import FileCollection
from processing.labeled_file_collection import LabeledFileCollection
from processing.labeled_file_container import LabeledFileContainer


class NodesFileSelector(FileSelector):
    """ Selects only .nodes.csv files as data files """

    def __init__(self, labels: dict=None):
        self.labels = labels

    def select(self, files: FileContainer) -> FileCollection:

        if isinstance(files, LabeledFileContainer):
            data_files = LabeledFileCollection()
            for label, file in files.glob_by_label("*.nodes.csv"):
                data_files.add(file, label)

            return data_files
        else:
            return FileList(files.glob("*.nodes.csv"))
