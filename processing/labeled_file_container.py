from processing.file_container import FileContainer


class LabeledFileContainer(FileContainer):
    """
    This is a file container that associates each file with a label. It
    provides methods to access the files using the corresponding label.
    """

    def __init__(self, directories: dict):
        self._directories = directories

    def __iter__(self):
        def iterator(directories):
            for directory in directories:
                for file in directory.iterdir():
                    yield file

        return iterator(self._directories.keys())

    def iter_by_label(self):
        """
        Returns iterator that iterates over each file and its corresponding
        label.
        """
        def iterator(directories: dict):
            """ Yields each file and its corresponding label """
            for directory, label in directories.items():
                for file in directory.iterdir():
                    yield file, label

        return iterator(self._directories)

    def glob(self, pattern: str):
        def iterator(directories, pattern):
            for directory in directories:
                for file in directory.glob(pattern):
                    yield file

        return iterator(self._directories.keys(), pattern)

    def glob_by_label(self, pattern: str):
        def iterator(directories, pattern):
            for directory, label in directories:
                for file in directory.glob(pattern):
                    yield file, label

        return iterator(self._directories.items(), pattern)
