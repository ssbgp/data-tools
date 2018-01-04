"""
SS-BGP Data Tools: Basic Data

Processes raw data from the simulator to obtain basic statistics.

For each dataset it computes:
- Number of samples
- Number of destinations
- Number of terminated and non-terminated destinations
- Average of termination times
- Average of message counts
- Average of deactivation counts

A destination is considered to have not terminated if at least one of its samples did not terminate.
The averages are computes over all samples, excluding only those which did not terminate.

Usage:
  basic-data <conf-file> [ --ignore-non-existing ] [ --out=<path> ]
  basic-data (-h | --help)
  basic-data (-V | --version)

Options:
  -h --help               Show this screen.
  -V --version            Show version.
  --ignore-non-existing   Ignore data directories specified in conf file that do not exist
  --out=<path>            Specify a custom output path. [Default: basic-data]

"""
import json
import sys
from pathlib import Path
from typing import Dict, List

import numpy as np
from collections import defaultdict
from docopt import docopt

from processing.application import Application
from processing.csv_printer import CSVPrinter
from processing.data_loader import DataLoader
from processing.data_processor import DataProcessor
from processing.directory import Directory
from processing.extension_selector import ExtensionFileSelector
from processing.labeled_file_collection import LabeledFileCollection
from processing.labeled_file_container import LabeledFileContainer
from processing.types import Label
from processing.utils import open_csv
from tools.utils import print_error


def main():
    args = docopt(__doc__, version="Basic Data v0.1")
    conf_path = Path(args['<conf-file>'])
    output_path = Path(args['--out'] + ".csv")

    if not conf_path.is_file():
        print_error(f"Configuration file was not found: {str(conf_path)}")
        sys.exit(1)

    data_sets = load_data_sets(conf_path)

    if not args['--ignore-non-existing']:
        # Make sure all data directories exist - If one does not, then exit
        for label, directory in data_sets.items():
            if not directory.is_dir():
                print_error(f"Data directory not found: {str(directory)}")
                sys.exit(1)

    # Setup the application
    app = Application(
        container=LabeledFileContainer(
            containers={label: Directory(data_dir) for label, data_dir in data_sets.items()}
        ),
        selector=ExtensionFileSelector(extension=".basic.csv"),
        loader=BasicDataLoader(),
        processor=BasicDataProcessor(printer=CSVPrinter(output_path))
    )

    return app.run()


def load_data_sets(conf_path: Path) -> Dict[Label, Path]:
    """
    Finds all data sets specified in the configuration file at *conf_path*.

    The configuration file is a JSON formatted file with a single object. Each pair of key and
    value corresponds to a data set. The key corresponds to the data set's label and the value to
    the data directory containing the files to load the data from.

    Example of a configuration file with two data sets:

        {
            "BGP": "/path/to/bgp/data",
            "SS-BGP": "/path/to/ss-bgp/data"
        }

    :return: a dictionary containing an entry for each data set
    """
    with open(conf_path) as file:
        return {label: Path(directory) for label, directory in json.load(file).items()}


class DestinationData:
    __slots__ = "sample_count", "terminations", "termination_times", "messages", "deactivations"

    def __init__(self):
        self.sample_count: int = 0
        self.terminations: List[bool] = []
        self.termination_times: List[int] = []
        self.messages: List[int] = []
        self.deactivations: List[int] = []


class BasicDataLoader(DataLoader):

    def load(self, data_files: LabeledFileCollection) -> Dict[Label, List[DestinationData]]:

        datasets: Dict[Label, List[DestinationData]] = defaultdict(list)
        for label, path in data_files.iter_by_label():
            data = DestinationData()
            with open_csv(path) as file:
                for row in file:
                    data.sample_count += 1

                    terminated = True if row["Terminated"] == "Yes" else False
                    data.terminations.append(terminated)

                    if terminated:
                        data.termination_times.append(int(row["Termination Time (Total)"]))
                        data.messages.append(int(row["Message Count"]))
                        data.deactivations.append(int(row["Detection Count"]))

            datasets[label].append(data)

        return datasets


class BasicDataProcessor(DataProcessor):

    def __init__(self, printer: CSVPrinter):
        self.printer = printer

    def process(self, datasets: Dict[Label, List[DestinationData]]):
        with self.printer:
            for label, dataset in datasets.items():
                destination_count = len(dataset)
                terminated_count = sum(int(all(dst.terminations)) for dst in dataset)

                self.printer.print_row({
                    "Dataset": label,
                    "Samples": sum(data.sample_count for data in dataset),
                    "Destinations": len(dataset),
                    "Terminated": terminated_count,
                    "Non-Terminated": destination_count - terminated_count,
                    "Termination Times (Avg.)":
                        np.average([value for dst in dataset for value in dst.termination_times]),
                    "Messages (Avg.)":
                        np.average([value for dst in dataset for value in dst.messages]),
                    "Deactivations (Avg.)":
                        np.average([value for dst in dataset for value in dst.deactivations]),
                })


if __name__ == '__main__':
    main()
