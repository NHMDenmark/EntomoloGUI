import sys
import json
import time
import imageio
import traceback
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QMutex

from utils import make_x_image, try_url
from guis.workers import WorkerSignals
from guis.progressDialog import progressDialog
from guis.basicGUI import basicGUI, ClickableIMG
from PyQt5.QtCore import QRunnable, pyqtSlot


class bigPiEyePreviewWorker(QRunnable):
    """
    Worker for getting a preview of the actual image (full resolution)
    This can be used for checking the focus of the camera.

    This is implemented as a worker thread so all the previews can load seperately and do not wait for eachother.
    """

    def __init__(self, camera_name):
        super(bigPiEyePreviewWorker, self).__init__()

        self.camera_name = (
            camera_name  # name / address of the camera, ie 'pieye-dragonfly.local'
        )
        self.signals = WorkerSignals()
        self.still_running = True  # used to stop the worker when the window is closed
        self.mutex = QMutex()

    @pyqtSlot()
    def run(self):
        """
        Initialise the runner function
        """
        while self.still_running:
            time.sleep(0.05)
            # Retrieve args/kwargs here; and fire processing using them
            try:
                result = self.getPreview()
            except:
                traceback.print_exc()
                exctype, value = sys.exc_info()[:2]
                self.signals.error.emit((exctype, value, traceback.format_exc()))
            else:
                self.signals.result.emit(result)  # Return the result of the processing

    def close(self):
        """close
        Stop the worker when the preview window is closed
        """
        self.mutex.lock()
        self.still_running = False  # ends the loops/worker above
        self.mutex.unlock()
        self.signals.finished.emit()

    def getPreview(self):
        """getPreview
        Query the PiEye API to take and cache an image,
        then request that image and display it

        Returns:
            data: a numpy array of the image.
        """
        # Tell the Pi-Eye to take and cache a new image
        take_img_url = f"http://{self.camera_name}:8080/takeAndCacheImage"
        response = try_url(take_img_url)

        # Check if it did not work - return None
        if response is None:
            return None

        # Otherwise take the returned image name and tell the API to
        #   get the cached image
        cached_img_name = json.loads(response.content)["image_name"]
        get_cached_img_url = (
            f"http://{self.camera_name}:8080/getCachedImage/{cached_img_name}"
        )
        response = try_url(get_cached_img_url)

        # Check if it did not work - return None
        if response is None:
            return None

        # If everything went well, return a numpy array of the image
        data = imageio.imread(response.content)
        return data


class bigPiEyePreviewGUI(basicGUI):
    """
    Opens a new window with a larger slower preview. This allows for dynamically adjusting the focus.
    Although the update is slow, as it asks the Pi-Eye to capture a full-resolution image each time.
    """

    def __init__(self, camera_name, worker):
        super().__init__()

        self.camera_name = camera_name
        self.worker = worker  # used to exit the worker when the window closes
        self.setWindowTitle(camera_name)

        # If for some reason cannot connect to the camera, show an image of an X instead
        self.x = make_x_image(width=320, height=240)

        self.img = QtWidgets.QLabel(self)
        self.img.setMaximumSize(4056, 3040)

        layout = QtWidgets.QVBoxLayout()
        self.label = QtWidgets.QLabel(
            "Below is a *almost* full resolution image from the pi-eye. Can be used for fine adjustments to focus. This does take about 10 seconds to update between images, so please be patient"
        )
        layout.addWidget(self.label)
        layout.addWidget(self.img)
        self.setLayout(layout)

    def closeEvent(self, event):
        """closeEvent
        Closes the window and exits the worker.
        Automatically triggered when the window is closed. (built in part of PyQt)
        """
        self.log.info(
            f"Telling big pi-eye ({self.camera_name}) preview worker to close"
        )
        self.worker.close()
        event.accept()

    def updatePreview(self, img):
        """updatePreview
        Update the image displayed in the GUI with a new image

        Args:
            img (numpy array): new image. If None, a large X is displayed instead.
        """
        if img is None:
            qImg = self.x
        else:
            height, width, _ = img.shape
            bytesPerLine = 3 * width
            qImg = QtGui.QImage(
                img.data,
                width,
                height,
                bytesPerLine,
                QtGui.QImage.Format_RGB888,
            )
        pixmap01 = QtGui.QPixmap.fromImage(qImg)
        preview_img = QtGui.QPixmap(pixmap01)
        preview_img = preview_img.scaled(
            4056 // 4, 3040 // 4, QtCore.Qt.KeepAspectRatio
        )

        self.img.setPixmap(preview_img)
