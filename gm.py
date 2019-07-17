# graphics_runner.py

from PySide2.QtWidgets import QApplication
from time import sleep, time
from PySide2.QtWidgets import QMainWindow


def _do_nothing():
    pass


class GraphicsRunner(object):
    def __init__(self):
        self._app = QApplication([])
        self._app.lastWindowClosed = _do_nothing
        self._window_to_run = None
        self._action_to_perform = _do_nothing
        self._still_running = True

    def set_window_to_run(self, window, action=None):
        if self._window_to_run:
            self._window_to_run.close()
        if action:
            self._action_to_perform = action
        self._window_to_run = window

    def get_running_window(self):
        return self._window_to_run

    def run(self, action=None):
        self._still_running = True
        while self._window_to_run.running() and self._still_running:
            start = time()
            self._window_to_run.show()

            if action:
                action()
            else:
                self._action_to_perform()

            self._app.processEvents()
            end = time()
            sleep(max([1.0/30 - (end - start), 0]))

    def stop(self):
        self._still_running = False
