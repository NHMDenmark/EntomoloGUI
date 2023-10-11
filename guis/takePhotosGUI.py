import sys
import traceback
import numpy as np
import pandas as pd

from time import sleep
from pathlib import Path
from datetime import datetime
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QSound
from PyQt5.QtCore import QRunnable, pyqtSlot, QThreadPool

from guis.cameraSetupGUI import JsonCameraSetting
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
                "/Users/dassco/Pi-Eyed-Piper/EntomoloGUI/media/Success.wav"
            ),  # Sound Byte from https://freesound.org/people/Thirsk/sounds/121104/
            "Failure": QSound(
                "/Users/dassco/Pi-Eyed-Piper/EntomoloGUI/media/Failure.wav"
            ),  # Sound Byte from https://freesound.org/people/Walter_Odington/sounds/25616/
        }

        self.jcs= JsonCameraSetting()
        self.storage_path = Path(storage_path)
        self.initUI()
        self.take_photos_timings = []
        self.save_photos_timings = []

    def initUI(self):
        self.takePhotosButton = QtWidgets.QPushButton("Take Photos")
        self.takePhotosButton.clicked.connect(self.takePhotos)
        self.takePhotosButton.setStyleSheet("background-color: #d6e6ff;")

        self.grid.addWidget(self.takePhotosButton, 0, 0, 10, 10)
        
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
        name = str(camera.camera_name)
        self.log.info("setting status finished " + name)
        self.results[camera.camera_name] = result
        self.finished[camera.camera_name] = True
        self.timing[camera.camera_name] = pd.Timestamp.now() - self.start_time

    def takePhotos(self):
        """takePhotos
        Tell all 7 cameras to take a photo, and wait for all the responses
        """
        self.log.info("Got Command to Take Photos")
        self.start_time = pd.Timestamp.now()
        # open progress dialog
        self.progress = progressDialog()
        self.progress._open()

        self.log.info("Started Taking Photos")

        # get list of all cameras
        canons = self.parent().canons.getCameras()
        pi_eyes = self.parent().piEyedPiper.getCameras()
        self.cameras = canons + pi_eyes

        camerasToRemove = []

        
        setting = getattr(self.jcs, "currentSetting")
        print(setting)
        
        for camera in self.cameras:
            print(camera)
            if setting[camera.camera_name] == False:
                camerasToRemove.append(camera)
        
        for camera in camerasToRemove:
            self.cameras.remove(camera)

        # dictionaries to store all results and status
        self.results = {}
        self.finished = {}
        self.timing = {}

        for camera in self.cameras:
            # initialize the camera as not finished
            self.finished[camera.camera_name] = False

            # create a worker to take a single photo from the camera
            worker = takeSinglePhotoWorker(camera)

            # when the worker is done, have it set its status to finished
            worker.signals.result.connect(self.setStatusFinished)

            # start the thread
            self.threadpool.start(worker)

        for i in range(5000):  # prevent infinite loop
            sleep(0.02)
            # get the number of cameras that have finished
            n_finished = sum(self.finished.values())

            # get the number of cameras that failed to return images
            n_failed = sum([x == None for x in self.results.values()])

            # calculate the percentage of cameras finished taking photos
            progress = int(100 * n_finished / len(self.finished))

            # update the progress bar
            self.progress.update(
                progress,
                f"{n_finished} / {len(self.finished)} photos taken, {n_failed} Failed",
            )

            # if all finished, close the loop
            if self.all_finished:
                break

        # get the number of cameras that failed to return images
        n_failed = sum([x == None for x in self.results.values()])

        # if all the images finished, save the photos
        if n_failed == 0:
            end_time = pd.Timestamp.now()
            self.timing['total'] = end_time - self.start_time
            self.take_photos_timings += [self.timing]
            pd.DataFrame(self.take_photos_timings).to_csv('take_photo_timings.csv')
            self.sounds["Success"].play()
            self.progress.update(
                100,
                f"All photos successfully taken.. Saving photos",
            )
            self.savePhotos(self.results)
        else:
            # play 'Failure' sound
            self.sounds["Failure"].play()
            # get names of cameras that failed
            failed_names = [k for k, v in self.results.items() if v == None]
            self.warn(
                f"Warning! The following cameras failed to take photos: {failed_names}, files not saved"
            )
        
        # close the progress window
        self.progress._close()

    def savePhotos(self, filenames):
        """savePhotos
        Given a dictionary of filenames for the cameras, save those files locally

        Args:
            filenames (dict): dictionary where the keys are the camera names, and the values are the file names
              of the images on the cameras themselves
        """
        self.start_time = pd.Timestamp.now()
        # folder name is just a unique identifier with the current timestamp
        folder_name = str(pd.Timestamp.now("UTC"))
        folder_path = self.storage_path / folder_name

        # create the new folder
        folder_path.mkdir(parents=True, exist_ok=False)

        # dictionaries to store status
        self.finished = {}
        self.timing = {}

        for camera in self.cameras:

            if filenames.get(camera.camera_name, None) is not None:
                # initialize the camera as not finished
                self.finished[camera.camera_name] = False

                # create a worker to take a single photo from the camera
                worker = saveSinglePhotoWorker(camera, filenames[camera.camera_name], folder_path)

                # when the worker is done, have it set its status to finished
                worker.signals.result.connect(self.setStatusFinished)

                # start the thread
                self.threadpool.start(worker)

        for i in range(5000):  # prevent infinite loop
            sleep(0.02)
            # get the number of cameras that have finished
            n_finished = sum(self.finished.values())

            # get the number of cameras that failed to return images
            n_failed = sum([x == None for x in self.results.values()])

            # calculate the percentage of cameras finished taking photos
            progress = int(100 * n_finished / len(self.finished))

            # update the progress bar
            self.progress.update(
                progress,
                f"{n_finished} / {len(self.finished)} photos saved, {n_failed} Failed",
            )

            # if all finished, close the loop
            if self.all_finished:
                break

        # get the number of cameras that failed to return images
        n_failed = sum([x == None for x in self.results.values()])

        self.log.info("Finished Saving photos in " + str(folder_path))

        # check that all photos were actually saved
        n_saved = len([x for x in folder_path.glob('*') if x.is_file()])

        if n_saved != len(self.cameras):
            self.warn('Something went wrong saving the files. Please check the save folder' + str(folder_path) + ', and/or contact support')

        
        end_time = pd.Timestamp.now()
        self.timing['total'] = end_time - self.start_time
        self.save_photos_timings += [self.timing]
        pd.DataFrame(self.save_photos_timings).to_csv('save_photo_timings.csv')


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
            out = [self.camera, result]
            self.signals.result.emit(out)
            self.signals.finished.emit()  # Done

class saveSinglePhotoWorker(QRunnable):
    """
    Worker thread for telling a single camera to save a photo.
      Threads are used here so we can simultaneously (asynchronously) tell all the
      cameras to take photos at once, and then the takePhotosWorker can wait for all the
      confirmations that the photo was taken, and once they all confirm the takePhotosWorker
      can tell the user that all photos were successfully taken. The photos then need to be
      moved to the local computer (this takes longer, so it is done separately)
    """

    def __init__(self, camera, camera_path, target_folder):
        super(saveSinglePhotoWorker, self).__init__()
        self.camera = camera
        self.camera_path = camera_path
        self.target_folder = target_folder
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        """
        Initialise the runner function with passed args, kwargs.
        """
        result = None
        try:
            if self.camera is not None:
                result = self.camera.savePhoto(self.camera_path, self.target_folder)  # Done
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        finally:
            out = [self.camera, result]
            self.signals.result.emit(out)
            self.signals.finished.emit()  # Done
