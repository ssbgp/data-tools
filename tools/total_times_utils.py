import numpy as np
import plotly.offline as plotly
from pathlib import Path
from plotly.graph_objs import Scatter

from processing.data_classes import Protocol
from processing.data_processor import DataProcessor


class TotalTimesProcessor(DataProcessor):
    """
    Expects a list of integer values. These integer values should represent the
    total times of each simulation in the data set.
    """

    def __init__(self, output_file: Path=Path("file.html"), print_results=False):
        self._output_file = output_file
        self._print_results = print_results

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

            if self._print_results:
                print(protocol)
                print("----------------------")
                print("data:", values)
                print("bins:", bin_edges)
                print("hist:", hist)
                print("cum:", cumsum)
                print()

            scatters.append(Scatter(x=bin_edges, y=cumsum,
                                    name=self.protocol_labels[protocol]))

        plotly.plot(scatters, filename=self._output_file, auto_open=False)
