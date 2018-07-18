import serial
from threading import Lock
from typing import List


class SerialListener:
    """SerialListener listens on provided port when `listen_on_serial(lock)` is called.
    To stop it, set flag in `stop_operation`"""
    def __init__(self, port_name: str, baud: int, stop_operation: bool):
        self._listener = serial.Serial(port=port_name,
                                       baudrate=baud,
                                       parity='N',
                                       stopbits=1,
                                       timeout=None,
                                       xonxoff=False,
                                       rtscts=False,
                                       dsrdtr=False)
        self._buffer = []
        self._stop_operation = stop_operation

    def get_buffer(self) -> List[int]:
        return self._buffer

    def listen_on_serial(self, lock: Lock) -> None:
        while True:
            if self._stop_operation['stopped']:
                exit(0)

            data = self._listener.read()
            with lock:
                self._buffer.append(int.from_bytes(
                    data, byteorder='big'))
