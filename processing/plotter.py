from pathlib import Path
from typing import NewType, Dict, Union, NamedTuple, List

import plotly.offline as plotly
from plotly.exceptions import PlotlyDictKeyError
from plotly.graph_objs import Scatter

from processing.errors import ProcessingError

TraceLine = NewType('TraceLine', Dict[str, Union[str, int]])


class TraceData(NamedTuple):
    label: str
    x: List[int]
    y: List[float]


class Plotter:

    def __init__(self, trace_lines: Dict[str, TraceLine], output: Path):
        self._trace_lines = trace_lines
        self._output_file = output

    def plot(self, traces: List[TraceData]):
        scatters: List[Scatter] = []
        for trace in traces:
            try:
                line = self._trace_lines.get(trace.label, {})
                scatters.append(Scatter(x=trace.x, y=trace.y, name=trace.label, line=line))
            except PlotlyDictKeyError as e:
                # Only the first line in the error message is relevant
                error_code = str(e).splitlines()[0]
                raise ProcessingError(f"trace configuration error: {error_code}")

        plotly.plot(scatters, filename=str(self._output_file), auto_open=False)
