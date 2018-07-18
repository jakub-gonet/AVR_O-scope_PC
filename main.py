from threading import Thread, Lock
from serialListener import SerialListener
from data import Data
from plotter import Plotter
from repeatedTimer import RepeatedTimer
from itertools import count
from sys import exit


def update_data(data, buffer, counter):
    data.update_data(buffer, lock, counter.__next__())


if __name__ == "__main__":
    settings = {'serial': {'serial_port': "/dev/ttyUSB0", 'baud': 4800},
                'plot': {'refresh_rate': 20,
                         'visible_s': 60,
                         'max_y': 5,
                         'color': 'g',
                         'x_capt': "Time", 'y_capt': "Measured value",
                         'title': "Atmega ADC output"},
                'data': {'max_value': 256,
                         'base_voltage': 5,
                         'stored_values_limit': 256000}
                }

    refresh_rate = settings['plot']['refresh_rate'] / 1000

    # variable for stopping threads
    stop_operation = {'stopped': False}

    # init lock for threads
    lock = Lock()

    # init data storages
    data = Data(settings['data'])

    # init serial communication
    serial_listener = SerialListener(
        settings['serial']['serial_port'], settings['serial']['baud'], stop_operation)

    # init plotting class
    plotter = Plotter(data, lock, settings['plot'])

    # get serial input buffer
    input_buffer = serial_listener.get_buffer()

    timer = count(start=refresh_rate, step=refresh_rate)

    serial_listener_thread = Thread(
        target=serial_listener.listen_on_serial, args=[lock])
    serial_listener_thread.start()
    data_updater_thread = RepeatedTimer(refresh_rate, update_data,
                                        *(data, input_buffer, timer))
    data_updater_thread.start()

    try:
        # start plotting
        plotter.plot()

        serial_listener_thread.join()

    except (KeyboardInterrupt):
        print("\nStopping...")
        stop_operation['stopped'] = True
        data_updater_thread.stop()
        plotter.exit()
        exit(0)
