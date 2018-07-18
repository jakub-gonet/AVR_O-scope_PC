import matplotlib.pyplot as plt
import matplotlib.animation as animation
from data import Data
from threading import Event
from threading import Lock
from itertools import count


class Plotter:
    """Plotter class is used to plot data provided from Data object. To start plotting call `start()`"""
    def __init__(self, data: Data, lock: Lock, plot_config: dict):
        self._figure = None
        self._axes = None
        self._animation = None
        self._line = None
        self._first_shown_time = 0
        self._data = data
        self._plot_config = plot_config
        self._lock = lock

    def plot(self) -> None:
        self._figure, self._axes = plt.subplots()
        self._config_axes()
        self._line, = self._axes.plot(self._data.get_t_data(),
                                      self._data.get_y_data(), self._plot_config["color"])

        self._animation = animation.FuncAnimation(self._figure, self._update, interval=self._plot_config["refresh_rate"],
                                                  blit=False)

        plt.show()

    def exit(self):
        plt.close()

    def _update(self, frame):
        t = self._data.get_t_data()
        y = self._data.get_y_data()
        time = self._data.get_current_time()

        if time >= self._first_shown_time + self._plot_config["visible_s"]:
            self._first_shown_time = time
            self._axes.set_xlim(time,
                                time + self._plot_config["visible_s"])
            self._axes.figure.canvas.draw()
        self._line.set_data(t, y)
        return self._line,

    def _config_axes(self) -> None:
        self._axes.set_ylim(-0.1, self._plot_config['max_y']+0.1)
        self._axes.set_xlim(0, self._plot_config['visible_s'])

        self._axes.minorticks_on()
        self._axes.grid()

        self._axes.set_xlabel(self._plot_config["x_capt"])
        self._axes.set_ylabel(self._plot_config["y_capt"])
        self._axes.set_title(self._plot_config["title"])
