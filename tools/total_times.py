"""
SS-BGP Data Tools: Total Times

Usage:
  plot-total-times [ --bgp=<bgp_dir> --ssbgp=<ssbgp_dir> --ssbgp2=<ssbgp2_dir ]
  plot-total-times (-h | --help)

Options:
  -h --help      Show this screen.
  -V --version   Show version.

"""
import csv
from collections import defaultdict

from docopt import docopt

from processing.application import Application
from processing.basic_file_selector import BasicFileSelector
from processing.data_classes import Protocol
from processing.data_loader import DataLoader
from processing.labeled_file_collection import LabeledFileCollection
from processing.labeled_file_container import LabeledFileContainer
from tools.total_times_utils import TotalTimesProcessor
from tools.utils import get_directory


class TotalTimesLoader(DataLoader):
    """
    Loads only the total times from all data files. Includes total times from
    simulations that did terminate and also simulations that did not terminate.
    """

    def load(self, data_files: LabeledFileCollection):
        # Container where data will be loaded to
        total_times = defaultdict(list)
        for protocol, data_file in data_files.iter_by_label():
            # Open the file as a CSV file
            with open(data_file) as file:
                for row in csv.DictReader(file, delimiter=";"):
                    total_time = int(row["Termination Time (Total)"])
                    total_times[protocol].append(total_time)

        return total_times


def main():
    args = docopt(__doc__, version="Total Times v0.1")

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
        selector=BasicFileSelector(),
        loader=TotalTimesLoader(),
        processor=TotalTimesProcessor()
    ).run()


if __name__ == '__main__':
    main()
