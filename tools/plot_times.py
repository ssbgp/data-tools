"""
SS-BGP Data Tools: Plot Termination Times

Usage:
  plot-times --traces <traces>... [ --out=<output>]
  plot-times (-h | --help)

Options:
  -h --help      Show this screen.
  -V --version   Show version.

"""
import sys
from collections import defaultdict
from pathlib import Path
from typing import Iterator, Tuple, List, Dict

import numpy as np
import plotly.offline as plotly
from docopt import docopt
from plotly.graph_objs import Scatter

from processing.application import Application
from processing.data_loader import DataLoader
from processing.data_processor import DataProcessor
from processing.directory import Directory
from processing.extension_selector import ExtensionFileSelector
from processing.files import open_csv
from processing.labeled_file_collection import LabeledFileCollection
from processing.labeled_file_container import LabeledFileContainer
from tools.utils import print_error


class TerminationTimesLoader(DataLoader):
    """
    Loads the termination times from each data file in collection *data_files*. Termination times
    are grouped by label. It includes termination times from simulations that did not terminate.
    """

    def load(self, data_files: LabeledFileCollection) -> Dict[str, List[int]]:
        # Container to hold the loaded data
        termination_times: Dict[str, List[int]] = defaultdict(list)

        for label, data_file in data_files.iter_by_label():
            # Load termination time from data file
            max_termination_time = 0
            with open_csv(data_file) as file:
                for row in file:
                    termination_time = int(row["Termination Time (Total)"])
                    max_termination_time = max(max_termination_time, termination_time)

            termination_times[label].append(max_termination_time)

        return termination_times


class TerminationTimesPlotter(DataProcessor):
    """
    Expects a list of integer values. These integer values should represent the
    total times of each simulation in the data set.
    """

    def __init__(self, output_file: Path):
        self._output_file = output_file

    def process(self, data: Dict[str, List[int]]):
        scatters = []
        for label, values in data.items():

            count = len(values)
            hist, bin_edges = np.histogram(values, bins=range(0, 2001000, 100))
            cumulative_sum = np.cumsum(hist)
            cumulative_sum = [(count - value) / count for value in cumulative_sum]

            scatters.append(Scatter(x=bin_edges, y=cumulative_sum, name=label))

        plotly.plot(scatters, filename=str(self._output_file), auto_open=False)


def traces_iter(traces: List[str]) -> Iterator[Tuple[str, Path]]:
    for trace in traces:
        label, data_dir = trace.split('=', maxsplit=1)
        yield label, Path(data_dir)


def main():
    args = docopt(__doc__, version="Plot Times v0.1")
    traces = {label: Directory(data_dir) for label, data_dir in traces_iter(args['<traces>'])}

    for directory in traces.values():
        if directory:
            if not directory.path.is_dir():
                print_error("data directory was not found:", directory)
                sys.exit(1)

    output_file = "plot.html" if not args['--out'] else args['--out']

    app = Application(
        container=LabeledFileContainer(
            directories={data_dir: label for label, data_dir in traces.items()}
        ),
        selector=ExtensionFileSelector(extension=".basic.csv"),
        loader=TerminationTimesLoader(),
        processor=TerminationTimesPlotter(Path(output_file))
    )

    return app.run()


if __name__ == '__main__':
    main()
