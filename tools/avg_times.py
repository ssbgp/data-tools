"""
SS-BGP Data Tools: Avg Times

Usage:
  plot-avg-times [ --bgp=<bgp_dir> --ssbgp=<ssbgp_dir> --ssbgp2=<ssbgp2_dir ]
  plot-avg-times (-h | --help)

Options:
  -h --help      Show this screen.
  -V --version   Show version.

"""
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
        return data_files


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

    def process(self, data_files: LabeledFileCollection):

        min_bin = 0
        max_bin = 2001000
        bin_step = 100

        bins = [i for i in range(min_bin, max_bin, bin_step)]
        value_counts = defaultdict(int)
        histograms = {}

        for protocol in data_files.labels():
            histograms[protocol] = [0] * (len(bins) - 1)

        file_count = len(data_files)
        file_n = 1
        for data_file, protocol in data_files.iter_by_label():
            print(f"\r  histogram:  file {file_n}/{file_count}", end="")
            file_n += 1

            # Open the file as a CSV file
            with open(data_file) as file:
                for value in map(int, file.readlines()):
                    histograms[protocol][int(value / bin_step)] += 1
                    value_counts[protocol] += 1

        scatters = []
        for protocol, hist in histograms.items():
            value_count = value_counts[protocol]
            cumsum = np.cumsum(hist)
            cumsum = [(value_count - value) / value_count for value in cumsum]

            print(protocol)
            print("----------------------")
            print("bins:", bins)
            print("hist:", hist)
            print("cum:", cumsum)
            print()

            scatters.append(Scatter(x=bins, y=cumsum,
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
        selector=ExtensionFileSelector(extension=".times.csv"),
        loader=AvgTimesLoader(),
        processor=AvgTimesProcessor()
    ).run()


if __name__ == '__main__':
    main()
