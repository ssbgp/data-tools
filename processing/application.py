from processing.data_loader import DataLoader
from processing.data_processor import DataProcessor
from processing.errors import ProcessingError
from processing.file_container import FileContainer
from processing.file_selector import FileSelector
from tools.utils import print_error


class Application:

    def __init__(self, container: FileContainer, selector: FileSelector,
                 loader: DataLoader, processor: DataProcessor):
        self.container = container
        self.selector = selector
        self.loader = loader
        self.processor = processor

    def run(self):
        try:
            print("Selecting files...")
            data_files = self.selector.select(self.container)
            print("Loading data...")
            data = self.loader.load(data_files)
            print("Processing...")
            self.processor.process(data)
            print("Completed successfully!")

        except ProcessingError as e:
            print_error(str(e))
            print("Failed!")
