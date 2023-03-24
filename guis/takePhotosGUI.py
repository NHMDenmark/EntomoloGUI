import sys
import traceback
import numpy as np
import pandas as pd

from time import sleep
from pathlib import Path
from PyQt5 import QtWidgets
from PyQt5.QtMultimedia import QSound
from PyQt5.QtCore import QRunnable, pyqtSlot, QThreadPool


from guis.basicGUI import basicGUI
from guis.workers import WorkerSignals
from guis.progressDialog import progressDialog


class takePhotosGUI(basicGUI):
    """takePhotosGUI
    GUI that controls taking photos and saving them
    """

    def __init__(self, storage_path, **kwargs):
        super(takePhotosGUI, self).__init__(**kwargs)

        # sounds used to verify if worked or not
        self.sounds = {
            "Success": QSound(
                "EntomoloGUI/media/Success.wav"
            ),  # Sound Byte from https://freesound.org/people/Thirsk/sounds/121104/
            "Failure": QSound(
                "EntomoloGUI/media/Failure.wav"
            ),  # Sound Byte from https://freesound.org/people/Walter_Odington/sounds/25616/
        }

        self.storage_path = Path(storage_path)
        self.initUI()

    def initUI(self):
        self.takePhotosButton = QtWidgets.QPushButton("Take Photos")
        self.takePhotosButton.clicked.connect(self.takePhotos)

        self.grid.addWidget(self.takePhotosButton, 0, 0, 1, 1)
        self.setLayout(self.grid)

    @property
    def all_finished(self):
        """all_finished

        Returns: True if all the cameras have finished taking photos (even if they failed)
          False otherwise.
        """
        finished = np.array(list(self.finished.values()))
        return finished.all()

    def setStatusFinished(self, camera_and_result):
        """setStatusFinished
        Once the camera has finished taking the photo, save the result (None if there was an error)
          and set the status to finished = True for that camera.

        Args:
            camera_and_result (list): list with two entries: the cameraGUI object and the result
              from the takePhoto function.
        """
        camera, result = camera_and_result
        print("setting status finished", camera.camera_name)
        self.results[camera.camera_name] = result
        self.finished[camera.camera_name] = True

    def takePhotos(self):
        self.sounds["Success"].play()
        self.log.info("Got Command to Take Photos")
        self.progress = progressDialog()
        self.progress._open()

        self.log.info("Started Taking Photos")

        canons = self.parent().canons.getCameras()
        pi_eyes = self.parent().piEyedPiper.getCameras()
        self.cameras = canons + pi_eyes

        self.results = {}
        self.finished = {}
        self.workers = {}

        for camera in self.cameras:
            self.finished[camera.camera_name] = False
            worker = takeSinglePhotoWorker(camera)
            worker.signals.result.connect(self.setStatusFinished)
            self.threadpool.start(worker)

        # CR: Kim to check how to do this waiting for all responses.
        i = 0
        while True:
            sleep(0.1)
            # print("self.finished", self.finished)
            n_finished = sum(self.finished.values())
            n_failed = sum([x == None for x in self.results.values()])
            progress = int(100 * n_finished / len(self.finished))
            self.progress.update(
                progress,
                f"{n_finished} / {len(self.finished)} cameras returned, {n_failed} Failed",
            )
            if self.all_finished:
                break

            # Prevents infinite loop if something goes wrong.
            i += 1
            if i > 5000:
                break

        self.progress._close()

        if self.all_finished or self.debug:
            self.sounds["Success"].play()
            self.savePhotos(self.results)

        if not self.all_finished:
            self.sounds["Failure"].play()
            failed_names = [k for k, v in self.results.items() if v == None]
            self.warn(
                "Warning! The following cameras failed to take photos:, files not saved"
            )

    def savePhotos(self, filenames):

        folder_name = str(pd.Timestamp.now("UTC"))
        folder_path = self.storage_path / folder_name

        folder_path.mkdir(parents=True, exist_ok=False)

        for camera in self.cameras:
            if filenames.get(camera.camera_name, None) is not None:
                camera.savePhoto(filenames[camera.camera_name], folder_path)

        print("Finished Saving photos")


class takeSinglePhotoWorker(QRunnable):
    """
    Worker thread for telling a single camera to take a photo.
      Threads are used here so we can simultaneously (asynchronously) tell all the
      cameras to take photos at once, and then the takePhotosWorker can wait for all the
      confirmations that the photo was taken, and once they all confirm the takePhotosWorker
      can tell the user that all photos were successfully taken. The photos then need to be
      moved to the local computer (this takes longer, so it is done separately)
    """

    def __init__(self, camera):
        super(takeSinglePhotoWorker, self).__init__()
        self.camera = camera
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        """
        Initialise the runner function with passed args, kwargs.
        """
        result = None
        try:
            if self.camera is not None:
                result = self.camera.takePhoto()  # Done
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        finally:
            print("Doing finally things for camera at ", self.camera.camera_name)
            out = [self.camera, result]
            self.signals.result.emit(out)
            self.signals.finished.emit()  # Done
