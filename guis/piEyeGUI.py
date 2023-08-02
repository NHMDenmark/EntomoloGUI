import cv2
import json
import imageio
import numpy as np
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QRunnable, pyqtSlot, QThreadPool
import tempfile
from pathlib import Path


from utils import try_url, make_x_image
from guis.workers import WorkerSignals, previewWorker
from guis.basicGUI import basicGUI, ClickableIMG
from guis.bigPiEyePreviewGUI import bigPiEyePreviewGUI, bigPiEyePreviewWorker


class piEyeGUI(basicGUI):
    """
    The GUI for each Pi-Eye. Contains most of the code for accessing the
      camera, taking photos, etc.

    Each Pi-Eye is a raspberry pi attached to a pi HQ camera. They run a local API
      server which connects to the computer through a USB-ethernet connection.

      We then query the API to get the camera preview and tell the pi to take an image
    """

    def __init__(self, address, **kwargs):
        super(piEyeGUI, self).__init__(**kwargs)

        # This is the ip address of the piEye on the local network. Usually something like "pieye-dragonfly.local"
        #   this is configured on the pi-eye itself. To change it, look up changing the hostname
        #   on a pi-zero.
        #   Accessing the previews is then something like: "http://pieye-ant.local:8080/camera/preview"
        self.address = address

        # If the camera disconnects, show a big x
        self.x = make_x_image(320, 240)

        self.initUI()
        self.startPreviewWorker()

    @property
    def camera_name(self):
        return self.address

    def initUI(self):
        self.title = QtWidgets.QLabel(f"{self.camera_name} Preview:")

        # The preview is a clickable image, so if you click the preview
        #   a new window will pop up, with a higher resolution slower version
        #   of the preview. This is to help with focussing the cameras.
        self.preview = ClickableIMG(self)
        self.preview.setMaximumSize(320, 240)
        self.preview.clicked.connect(self.openFocusedPreviewWindow)

        self.grid.addWidget(self.title, 0, 0, 1, 1)
        self.grid.addWidget(self.preview, 2, 0, 1, 1)

        self.setLayout(self.grid)

    def takePhoto(self):
        """takePhoto

        Takes a photo and saves it to a temporary folder on this computer.
        Returns:
            The name of the image that was taken, or None if there was an error

        """
        take_img_url = f"http://{self.camera_name}:8080/camera/still-capture"
        response = try_url(take_img_url)
        self.log.info(f"Taking pi-eye photo {self.camera_name}")
        if response is None:
            self.log.warn(f"No Response for pi-eye at address {self.camera_name}")
            return None
        else:
            tmpdir = Path(tempfile.gettempdir())

            # get filename from response
            filename = response.json()["filename"]
            filepath = tmpdir / filename
            open(filepath, "wb").write(response.content)

            return filepath

    def savePhoto(self, filepath, folder):
        """savePhoto

        Moves the photo from the temporary folder to the folder specified, with the name specified.

        """
        # open file at filepath
        # save it to folder with name
        try:
            self.log.info(f"Saving photo {filepath} to {folder}")
            filename = Path(filepath).name
            newpath = Path(folder) / filename

            # move file to new location
            Path(filepath).rename(newpath)

        except:
            self.log.warn(f"Could not save photo {filepath} to {folder}")
            return False

    def openFocusedPreviewWindow(self):
        """openFocusedPreviewWindow
        Opens a new window with a larger slower preview. This allows for dynamically adjusting the focus.
        Although the update is slow, as it asks the Pi-Eye to capture a full-resolution image each time.
        """
        self.log.info("Opening Focused Pi-Eye Preview Window")
        self.big_preview_worker = bigPiEyePreviewWorker(self.camera_name)

        self.big_preview = bigPiEyePreviewGUI(self.camera_name, self.big_preview_worker)
        self.big_preview.show()

        self.big_preview_worker.signals.result.connect(self.big_preview.updatePreview)
        self.threadpool.start(self.big_preview_worker)

    def closeEvent(self, event):
        """closeEvent
        Closes the window and exits the worker.
        Automatically triggered when the window is closed. (built in part of PyQt)
        """
        self.log.info(f"Telling pi-eye ({self.camera_name}) preview worker to close")
        self.preview_worker.close()
        event.accept()

    def startPreviewWorker(self):
        """startPreviewWorker
        In order for all the previews to update asynchronously we give each
        preview its own worker thread. This worker thread will run the updatePreview function below
        """
        self.preview_worker = previewWorker(self)
        self.preview_worker.signals.result.connect(self.updatePreview)
        self.threadpool.start(self.preview_worker)

    def getPreview(self):
        """getPreview
        Get the preview from the Pi-Eye url. If something goes wrong, return None
        """
        self.preview_url = f"http://{self.camera_name}:8080/camera/preview"
        response = try_url(self.preview_url)

        if response is None:
            return None
        else:
            data = imageio.imread(response.content)
            return data

    def updatePreview(self, img):
        """updatePreview
        Given an image as a numpy array, update the preview in the GUI.
          If something went wrong with getting the image, the image will be None.
          Then this function updates the preview to show a giant X
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
        preview_img = preview_img.scaled(150, 150, QtCore.Qt.KeepAspectRatio)

        self.preview.setPixmap(preview_img)
