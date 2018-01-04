"""
SS-BGP Data Tools: Plot Termination Times

Computes the inverse cumulative sum of the destinations' termination time for multiple datasets.

The termination time of a destination corresponds to the highest termination time among all of
its samples.

Usage:
  inv-cumsum <conf-file> [ --out=<path> ]
  inv-cumsum (-h | --help)

Options:
  -h --help      Show this screen.
  -V --version   Show version.
  --out=<path>   Specify a custom output path. [Default: inv-cumsum]

"""
import json
import sys
from pathlib import Path
from typing import List, Dict, NamedTuple

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
from processing.plotter import Plotter, TraceLine, TraceData
from processing.types import Label
from processing.utils import open_csv
from tools.utils import print_error


def main():
    args = docopt(__doc__, version="Plot Times v0.1")
    output_path = args['--out']

    traces = load_traces(args['<conf-file>'])

    # Check if all data directories actually exist
    for trace in traces:
        if not trace.data_dir.path.is_dir():
            print_error(f"data directory not found: {str(trace.data_dir)}")
            sys.exit(1)

    # Setup the application
    app = Application(
        container=LabeledFileContainer(
            containers={trace.label: trace.data_dir for trace in traces}
        ),
        selector=ExtensionFileSelector(extension=".basic.csv"),
        loader=TerminationTimesLoader(),
        processor=TerminationTimesProcessor(
            plotter=Plotter(
                trace_lines={trace.label: trace.line for trace in traces},
                output=Path(output_path + '.html')
            ),
            printer=CSVPrinter(Path(output_path + '.csv'))
        )
    )

    return app.run()


class Trace(NamedTuple):
    label: str
    data_dir: Directory
    line: TraceLine = {}


def load_traces(path: Path) -> List[Trace]:
    """
    Loads traces from a trace file. The trace file is a JSON file that specifies some
    configurations for each trace. For example,

        "TRACE LABEL": {
            "data": "/path/to/data",
            "line": {
                "color": "rgb(205, 12, 24)",
                "dash": "dot"
            }
        }

    'TRACE LABEL' corresponds to the label of the trace and must be unique to each trace.
    Each trace has two main attributes:
        - data: corresponds to the data directory (its value is '/path/to/data' in the example)
        - line: specifies a set of attributes to describe how the line is displayed

    A trace file may have multiple traces.

    """
    with open(path) as file:
        traces: List[Trace] = []
        for label, specs in json.load(file).items():
            trace = Trace(label, Directory(Path(specs['data'])), specs['line'])
            traces.append(trace)

        return traces


def parse_traces(trace_pairs: List[str]) -> List[Trace]:
    """
    Takes a list of trace pairs and returns a list of trace instances corresponding to those pairs.
    A trace pair is composed of a string with the trace's label and data directory separated by
    an equals sign. For example,

        - Exp1=/path/to/data -> label is 'Exp1' and data directory is '/path/to/data'
        - Exp1=/path=to/data -> label is 'Exp1' and data directory is '/path=to/data'
        - Exp1=path/to/data -> label is 'Exp1' and data directory is 'path=to/data'
        - Ex=p1=/path/to/data -> label is 'Ex' and data directory is 'p1=/path/to/data'

    """
    traces: List[Trace] = []
    for pair in trace_pairs:
        label, data_dir = pair.split('=', maxsplit=1)
        traces.append(Trace(label, Directory(Path(data_dir))))

    return traces


class TerminationTimesLoader(DataLoader):
    """
    Loads the termination times from each data file in collection *data_files*. For each data
    file it considers only the maximum of all termination times among all samples (seeds).

    Termination times are grouped by label.
    It includes termination times from simulations that did not terminate.
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


class TerminationTimesProcessor(DataProcessor):
    """
    Expects a list of termination times (integer values) for each label.
    For each label, it computes the cumulative sum and plots it using the specified plotter.
    """

    def __init__(self, plotter: Plotter = None, printer: CSVPrinter = None):
        self._plotter = plotter
        self._printer = printer

    def process(self, data: Dict[str, List[int]]):

        #
        # Compute the traces for each data input
        #
        traces: Dict[Label, List[float]] = {}
        x = list(range(0, 2001000, 100))
        for label, values in data.items():
            count = len(values)
            hist, bin_edges = np.histogram(values, bins=x)
            cumulative_sum = np.cumsum(hist)
            # Convert the cumulative sum to a relative cumulative sum
            cumulative_sum = [(count - value) / count for value in cumulative_sum]

            traces[label] = cumulative_sum

        #
        # Plot all traces
        #
        if self._plotter:
            self._plotter.plot(traces=[TraceData(label, x, y) for label, y in traces.items()])

        #
        # Output trace values to a table
        #
        if self._printer:
            with self._printer:
                labels = list(traces.keys())
                bins_label = "Bins (x)"
                self._printer.set_headers(headers=[bins_label] + labels)

                for i, value in enumerate(x[:-1]):
                    row = {label: traces[label][i] for label in labels}
                    row[bins_label] = value
                    self._printer.print_row(row)

                # The last value in 'x' is the last edge, for which there is not value
                self._printer.print_row({bins_label: x[-1]})


if __name__ == '__main__':
    main()
