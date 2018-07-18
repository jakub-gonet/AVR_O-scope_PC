from collections import deque
from threading import Lock
from typing import List
from itertools import count


class Data:
    """Data class is used to store measured data. Use `update_data(buffer, lock, current_time)` to update data."""
    def __init__(self, config: dict):
        self._config = config
        self._y_data = deque([0], config['stored_values_limit'])
        self._t_data = deque([0], config['stored_values_limit'])
        self._current_time = 0

    def get_y_data(self) -> deque:
        return self._y_data

    def get_t_data(self) -> deque:
        return self._t_data

    def get_current_time(self) -> float:
        return self._current_time

    def _change_measured_units(self, values: List[int]):
        return [(x/self._config['max_value'])*self._config['base_voltage'] for x in values]

    def update_data(self, buffer: List[int], lock: Lock, current_time: float) -> None:
        self._current_time = current_time
        with lock:
            y = list(buffer)
            buffer.clear()
        y = self._change_measured_units(y)
        last_t = self._t_data[-1]
        t = self._create_time_data_values(len(y), last_t, current_time)

        self._y_data += y
        self._t_data += t

    def _create_time_data_values(self, values_amount: int, last_t: float, current_t: float) -> List[float]:
        if values_amount <= 0:
            return []
        t = []
        assert last_t < current_t, f"Current time ({current_t}) is before or the same as previous provided time ({last_t})"
        delta_t = current_t - last_t
        times = count(start=last_t, step=delta_t/values_amount)

        for _i, time in zip(range(values_amount), times):
            t.append(time)
        return t
