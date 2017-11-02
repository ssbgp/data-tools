from pathlib import Path


# Interface
class FileSelector:
    """
    File selectors are responsible for selecting data files.
    The implementation specifies how and which files are selected.
    """

    def select(self, directory: Path) -> list:
        """
        Selects data files from the specified directory.

        :param directory: path to directory to look for data files
        :return: list containing all data files selected
        """
