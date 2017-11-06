from processing.data_loader import DataLoader
from processing.data_processor import DataProcessor
from processing.file_container import FileContainer
from processing.file_selector import FileSelector


class Application:

    def __init__(self, container: FileContainer, selector: FileSelector,
                 loader: DataLoader, processor: DataProcessor):
        self.container = container
        self.selector = selector
        self.loader = loader
        self.processor = processor

    def run(self):
        data_files = self.selector.select(self.container)
        data = self.loader.load(data_files)
        self.processor.process(data)
