"""
SS-BGP Data Tools: Count Terminations

Counts the number of terminated and non-terminated destinations.

It looks for '.basic.csv' files inside the specified data directories. Each one of these files is
considered to be a single destination. A destination is considered terminated if every sample
terminated, that is, if all samples have a value of "True" set for the "Terminated" column of the
corresponding data file.

Usage:
  count-terminations <conf-file> [ --ignore-non-existing ]
  count-terminations (-h | --help)
  count-terminations (-V | --version)

Options:
  -h --help               Show this screen.
  -V --version            Show version.
  --ignore-non-existing   Ignore data directories specified in conf file that do not exist

"""
import json
import sys
from pathlib import Path
from typing import Dict, List

import numpy as np
from collections import defaultdict
from docopt import docopt

from processing.application import Application
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
        loader=TerminationsDataLoader(),
        processor=TerminationsDataProcessor()
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


class Data:
    __slots__ = "sample_count", "terminations"

    def __init__(self):
        self.sample_count: int = 0
        self.terminations: List[bool] = []


class TerminationsDataLoader(DataLoader):

    def load(self, data_files: LabeledFileCollection) -> Dict[Label, List[Data]]:

        destinations: Dict[Label, List[Data]] = defaultdict(list)
        for label, path in data_files.iter_by_label():
            data = Data()
            with open_csv(path) as file:
                for row in file:
                    terminated = True if row["Terminated"] == "Yes" else False
                    data.terminations.append(terminated)
                    data.sample_count += 1

            destinations[label].append(data)

        return destinations


class TerminationsDataProcessor(DataProcessor):

    def process(self, simulations: Dict[Label, List[Data]]):
        for label, data_items in simulations.items():
            destination_count = len(data_items)
            terminated_count = sum(int(all(data.terminations)) for data in data_items)

            print(label)
            print("  Avg. sample count:", np.average([data.sample_count for data in data_items]))
            print("  Destination count:", destination_count)
            print("  Terminated count:", terminated_count)
            print("  Non-terminated count:", destination_count - terminated_count)
            print()


if __name__ == '__main__':
    main()
