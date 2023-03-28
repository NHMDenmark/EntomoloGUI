import io
import sys
import time
import json
import traceback
import gphoto2 as gp
import pandas as pd

from utils import try_url, make_x_image
from PyQt5.QtCore import pyqtSignal, QObject, QRunnable, pyqtSlot, QThreadPool

from PIL import Image
from time import sleep
from PIL.ImageQt import ImageQt

# Worker Signals framework from https://www.pythonguis.com/tutorials/multithreading-pyqt-applications-qthreadpool/
class WorkerSignals(QObject):
    """
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    progress
        int indicating % progress

    """

    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class previewWorker(QRunnable):
    """
    Worker thread
    """

    def __init__(self, gui):
        super(previewWorker, self).__init__()
        self.gui = gui
        # Store constructor arguments (re-used for processing)
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        """
        Initialise the runner function with passed args, kwargs.
        """
        while True:
            sleep(0.05)
            # Retrieve args/kwargs here; and fire processing using them
            try:
                result = self.gui.getPreview()
            except:
                pass
                #traceback.print_exc()
                #exctype, value = sys.exc_info()[:2]
                #self.signals.error.emit((exctype, value, traceback.format_exc()))
            else:
                self.signals.result.emit(result)  # Return the result of the processing
