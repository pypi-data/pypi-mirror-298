from pathlib import Path

from iccore.serialization import read_json
from icplot.graph import LinePlotSeries
from icplot.graph.matplotlib import MatplotlibPlotter
from ictasks.tasks import TaskCollection


class PlotGenerator:
    def __init__(
        self,
        tasks: TaskCollection,
        plots: dict,
        colormap: dict,
        series_label: str,
        x_axis: str,
        result_filename: str,
        result_dir: Path,
    ):
        self.tasks = tasks
        self.results: list[dict] = []
        self.plotter = MatplotlibPlotter()
        self.plots = plots
        self.colormap = colormap
        self.series_label = series_label
        self.x_axis = x_axis
        self.result_filename = result_filename
        self.result_dir = result_dir

    def get_x_y(self, result, plot_key):
        xval = int(result[self.x_axis])
        if plot_key == "runtime":
            start_time = result["start_time"]
            end_time = result["end_time"]
            return xval, (end_time - start_time)

    def sort(self, x, y):
        """
        Sorts x and y lists by the x values
        """

        tuples = list(zip(x, y))
        tuples.sort(key=lambda tup: tup[0])
        for idx, _ in enumerate(tuples):
            x[idx] = tuples[idx][0]
            y[idx] = tuples[idx][1]

    def plot_label(self, label: str):
        if label in self.colormap:
            color = self.colormap[label]
        else:
            color = None

        x_vals = []
        y_vals = []
        for result in self.results:
            if result["state"] == "finished" and result["circuit_label"] == label:
                for plot_key in self.plots.keys():
                    x, y = self.get_x_y(result, plot_key)
                    x_vals.append(x)
                    y_vals.append(y)
        self.sort(x_vals, y_vals)

        for plot_key in self.plots.keys():
            if label in self.colormap:
                series = LinePlotSeries(
                    x=x_vals, y=y_vals, label=label, highlight=True, color=color
                )
            else:
                series = LinePlotSeries(x=x_vals, y=y_vals, label=label)
            self.plots[plot_key].add_series(series)

    def make_plots(self):
        for task in self.tasks:
            task_dir = task.get_task_dir()
            if (task_dir / self.result_filename).is_file():
                self.results.append(read_json(task_dir / self.result_filename))

        labels = set()
        for result in self.results:
            labels.add(result[self.series_label])

        for label in labels:
            self.plot_label(label)

        for key, plot in self.plots.items():
            self.plotter.plot(plot, self.result_dir / f"{key}.svg")
