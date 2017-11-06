from processing.data_loader import DataLoader
from processing.data_processor import DataProcessor
from processing.file_collection import FileCollection
from processing.file_selector import FileSelector


class Application:

    def __init__(self, selector: FileSelector, loader: DataLoader,
                 processor: DataProcessor):
        self.selector = selector
        self.loader = loader
        self.processor = processor

    def run(self, files: FileCollection):
        data_files = self.selector.select(files)
        data = self.loader.load(data_files)
        self.processor.process(data)
