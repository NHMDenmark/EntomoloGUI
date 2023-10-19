import sip
import sys
import traceback
from time import sleep
from PyQt5.QtCore import pyqtSignal, QObject, QRunnable, pyqtSlot, QThreadPool, QMutex


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
    hi
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
        self.still_running = True  # used to stop the worker when the window is closed
        self.mutex = QMutex()

    def close(self):
        """close
        Stop the worker when the preview window is closed
        """
        self.mutex.lock()
        self.still_running = False  # ends the loops/worker above
        self.mutex.unlock()
        self.signals.finished.emit()

    @pyqtSlot()
    def run(self):
        """
        Initialise the runner function.
        """
        
        while self.still_running:
            sleep(0.05)
            try:
                result = self.gui.getPreview()
            except:
                traceback.print_exc()
                exctype, value = sys.exc_info()[:2]
                self.signals.error.emit((exctype, value, traceback.format_exc()))
            else:
                if not sip.isdeleted(self.signals):
                    self.signals.result.emit(result)  # Return the result of the processing
