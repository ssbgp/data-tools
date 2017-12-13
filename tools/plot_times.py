"""
SS-BGP Data Tools: Plot Termination Times

Usage:
  plot-times --traces <traces>... [ --out=<output>]
  plot-times --file=<file> [ --out=<output>]
  plot-times (-h | --help)

Options:
  -h --help      Show this screen.
  -V --version   Show version.

"""
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import List, Dict, NamedTuple, NewType, Union

import numpy as np
import plotly.offline as plotly
from docopt import docopt
from plotly.exceptions import PlotlyDictKeyError
from plotly.graph_objs import Scatter

from processing.application import Application
from processing.data_loader import DataLoader
from processing.data_processor import DataProcessor
from processing.directory import Directory
from processing.errors import ProcessingError
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


TraceLine = NewType('TraceLine', Dict[str, Union[str, int]])


class Trace(NamedTuple):
    label: str
    data_dir: Directory
    line: TraceLine = {}


class TraceData(NamedTuple):
    label: str
    x: List[int]
    y: List[float]


class TerminationTimesPlotter(DataProcessor):
    """
    Expects a list of integer values. These integer values should represent the
    total times of each simulation in the data set.
    """

    def __init__(self, output_file: Path, trace_lines: Dict[str, TraceLine]):
        self._output_file = output_file
        self._trace_lines = trace_lines

    def process(self, data: Dict[str, List[int]]):

        #
        # Compute the traces for each data input
        #
        traces: List[TraceData] = []
        for label, values in data.items():
            count = len(values)
            hist, bin_edges = np.histogram(values, bins=range(0, 2001000, 100))
            cumulative_sum = np.cumsum(hist)
            cumulative_sum = [(count - value) / count for value in cumulative_sum]

            traces.append(TraceData(label, x=bin_edges, y=cumulative_sum))

        #
        # Plot each trace
        #
        scatters: List[Scatter] = []
        for trace in traces:
            line = self._trace_lines.get(trace.label, {})

            try:
                scatters.append(Scatter(x=trace.x, y=trace.y, name=trace.label, line=line))
            except PlotlyDictKeyError as e:
                message, *_ = str(e).split('\n')
                raise ProcessingError(f"trace configuration error: {message}")

        plotly.plot(scatters, filename=str(self._output_file), auto_open=False)


def load_traces(path: Path) -> List[Trace]:
    """ Loads traces from a trace file """
    with open(path) as file:
        traces: List[Trace] = []
        for label, specs in json.load(file).items():
            trace = Trace(label, Directory(Path(specs['data'])), specs['line'])
            traces.append(trace)

        return traces


def parse_traces(trace_pairs: List[str]) -> List[Trace]:
    """
    Takes a list of trace pairs and returns a list of trace instances corresponding to those
    pairs.
    """
    traces: List[Trace] = []
    for pair in trace_pairs:
        label, data_dir = pair.split('=', maxsplit=1)
        traces.append(Trace(label, Directory(Path(data_dir))))

    return traces


def main():
    args = docopt(__doc__, version="Plot Times v0.1")

    output_file = "plot.html" if not args['--out'] else args['--out']

    if args['--traces']:
        traces = parse_traces(args['<traces>'])
    else:
        traces = load_traces(args['--file'])

    # Check if all data directories actually exist
    for trace in traces:
        if not trace.data_dir.path.is_dir():
            print_error(f"data directory not found: {str(trace.data_dir)}")
            sys.exit(1)

    # Setup the application
    app = Application(
        container=LabeledFileContainer(
            directories={trace.data_dir: trace.label for trace in traces}
        ),
        selector=ExtensionFileSelector(extension=".basic.csv"),
        loader=TerminationTimesLoader(),
        processor=TerminationTimesPlotter(
            output_file=Path(output_file),
            trace_lines={trace.label: trace.line for trace in traces}
        )
    )

    return app.run()


if __name__ == '__main__':
    main()
