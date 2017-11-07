"""
SS-BGP Data Tools: Avg Times

Usage:
  plot-avg-times [ --bgp=<bgp_dir> --ssbgp=<ssbgp_dir> --ssbgp2=<ssbgp2_dir ]
  plot-avg-times (-h | --help)

Options:
  -h --help      Show this screen.
  -V --version   Show version.

"""
import csv
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
import plotly.offline as py
from docopt import docopt
from plotly.graph_objs import Scatter

from processing.application import Application
from processing.data_classes import Protocol
from processing.data_loader import DataLoader
from processing.data_processor import DataProcessor
from processing.directory import Directory, EmptyDirectory
from processing.extension_selector import ExtensionFileSelector
from processing.labeled_file_collection import LabeledFileCollection
from processing.labeled_file_container import LabeledFileContainer
from tools.utils import print_error


class AvgTimesLoader(DataLoader):
    """
    Loads only the average times from all data files. Includes average times
    from simulations that did terminate and also simulations that did not
    terminate.
    """

    def load(self, data_files: LabeledFileCollection):
        # Container where data will be loaded to
        avg_times = defaultdict(list)
        for protocol, data_file in data_files.iter_by_label():
            # Open the file as a CSV file
            with open(data_file) as file:
                for row in csv.DictReader(file, delimiter=";"):
                    avg_time = float(row["Termination Time (Avg.)"])
                    avg_times[protocol].append(avg_time)

        return avg_times


class AvgTimesProcessor(DataProcessor):
    """
    Expects a list of integer values. These integer values should represent the
    average times of each simulation in the data set.
    """

    protocol_labels = {
        Protocol.BGP: "BGP",
        Protocol.SSBGP: "SSBGP",
        Protocol.SSBGP2: "SS-BGP2",
    }

    def process(self, data: dict):
        scatters = []
        for protocol, values in data.items():
            count = len(values)
            hist, bin_edges = np.histogram(values, bins=range(0, 2001000, 100))
            cumsum = np.cumsum(hist)
            cumsum = [(count - value) / count for value in cumsum]

            print(protocol)
            print("----------------------")
            print("data:", values)
            print("bins:", bin_edges)
            print("hist:", hist)
            print("cum:", cumsum)
            print()

            scatters.append(Scatter(x=bin_edges, y=cumsum,
                                    name=self.protocol_labels[protocol]))

        py.plot(scatters, filename="file.html", auto_open=False)


def get_directory(args: dict, key: str):
    if args[key] is None:
        return EmptyDirectory()

    directory = Directory(Path(args[key]))

    if directory:
        if not directory.path.is_dir():
            print_error("data directory was not found:", directory)
            sys.exit(1)

    return directory


def main():
    args = docopt(__doc__, version="Avg Times v0.1")

    bgp_directory = get_directory(args, '--bgp')
    ssbgp_directory = get_directory(args, '--ssbgp')
    ssbgp2_directory = get_directory(args, '--ssbgp2')

    Application(
        container=LabeledFileContainer(
            directories={
                bgp_directory: Protocol.BGP,
                ssbgp_directory: Protocol.SSBGP,
                ssbgp2_directory: Protocol.SSBGP2,
            }
        ),
        selector=ExtensionFileSelector(extension=".basic.csv"),
        loader=AvgTimesLoader(),
        processor=AvgTimesProcessor()
    ).run()


if __name__ == '__main__':
    main()
