import io

import gphoto2 as gp
from PIL import Image
from time import sleep
from PIL.ImageQt import ImageQt

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QMutex
from guis.workers import previewWorker
from guis.basicGUI import basicGUI, ClickableIMG
from utils import make_x_image


class canonGUI(basicGUI):
    """
    The GUI for each Canon camera. Contains most of the code for accessing the
      camera, taking photos, etc.
    """

    def __init__(self, location, **kwargs):
        super(canonGUI, self).__init__(**kwargs)
        self.location = location

        # Used to prevent multiple threads from accessing the same data at once
        self.mutex = QMutex()

        # the gphoto2 instance of the camera controller
        self.controller = self.getController(owner=location)

        # the preview cannot work if the camera is set to raw format
        self.setImageFormatJPEG()

        # flag used to stop the preview when the camera is taking a photo
        self.pause_preview = False
        self.preview_paused = False

        # if the camera cannot provide a preview, or the camera cannot be found, display an x instead
        self.x = make_x_image(640, 420)

        self.initUI()

        # start the preview worker thread
        self.startPreviewWorker()

    def set_pause_preview(self, val):
        """set_pause_preview
        Threadsafe way to set the value of the pause_preview flag.

        Args:
            val (bool): True or False
        """
        self.mutex.lock()
        self.pause_preview = val
        self.mutex.unlock()
        while self.preview_paused != True:
            print('waiting for preview to be actually paused')
            sleep(0.05)

    @property
    def camera_name(self):
        """camera_name

        Returns:
            self.location: the name of the canon camera. Either 'Top' or 'Side' specifying where it is
        """
        return self.location

    def initUI(self):
        """initUI
        initializes the UI for the canon camera
        """
        self.title = QtWidgets.QLabel(f"{self.camera_name} Canon Preview:")

        self.preview = ClickableIMG(self)
        self.preview.setMaximumSize(640, 420)
        self.preview.clicked.connect(self.openIMG)

        self.grid.addWidget(self.title, 0, 0, 1, 1)
        self.grid.addWidget(self.preview, 2, 0, 1, 1)

        self.setLayout(self.grid)

    def reinitCamera(self):
        """reinitCamera
        Attempts to reinitialize the camera. This is necessary in case something goes wrong with the connection
        For example, if a camera is unplugged.
        """
        if self.controller is not None:
            self.pause_preview = True
            print('Shutting Down ADDRESS:',self.camera_name)
            gp.check_result(gp.gp_camera_exit(self.controller))

        self.controller = self.getController(owner=self.location)
        self.setImageFormatJPEG()
        self.pause_preview = False

    def startPreviewWorker(self):
        """startPreviewWorker
        Start the preview worker thread and add it to the overall threadpool.
        This preview worker runs the updatePreview function below.
        """
        self.preview_worker = previewWorker(self)
        self.preview_worker.signals.result.connect(self.updatePreview)
        self.threadpool.start(self.preview_worker)

    def updatePreview(self, img):
        """updatePreview
        Updates the GUI with a new image

        Args:
            img (numpy array): new image. if None, show a large x
        """

        # if the image is none, a large x is displayed
        if img is None:
            img = self.x

        # update the GUI image
        pixmap01 = QtGui.QPixmap.fromImage(img)
        preview_img = QtGui.QPixmap(pixmap01)
        preview_img = preview_img.scaled(640, 420, QtCore.Qt.KeepAspectRatio)
        self.preview.setPixmap(preview_img)

    def openIMG(self):
        """openIMG
        Future potential functionality - like the Pi-Eyes, could be used to open a large
        preview of a single camera to do fine-tuned focussing.
        """
        pass

    def getController(self, owner):
        """getController
        Get a class instance of the gphoto2 camera controller for the desired canon camera

        Args:
            owner (str): The 'owner' of the camera - Defined on the camera itself.
               Ensures that we find the correct camera.

        Returns:
            controller or None: returns an instance of the gphoto2 camera controller or None if unable to find the camera
        """
        # get a list of all cameras gphoto2 can detect
        cameras = gp.Camera.autodetect()

        # filter this list by those that are the correct model
        canons = [x for x in cameras if x[0] == "Canon EOS R5"]

        # loop over each canon camera and look for the one with the correct 'Owner'/'Location' ('Top' or 'Side')
        for cam_data in canons:
            model, port = cam_data

            # load all the ports
            port_info_list = gp.PortInfoList()
            port_info_list.load()

            # load all the abilities
            abilities_list = gp.CameraAbilitiesList()
            abilities_list.load()

            # create a camera instance
            cam = gp.check_result(gp.gp_camera_new())

            # set said camera instance to look at the port we are interested in
            idx = port_info_list.lookup_path(port)
            cam.set_port_info(port_info_list[idx])

            # set said camera instance to have the abilities of the model we are interested in
            idx = abilities_list.lookup_model(model)
            cam.set_abilities(abilities_list[idx])

            # try initializing the camera in question
            OK = gp.gp_camera_init(cam)
            if OK >= gp.GP_OK:
                # if that worked, get the 'owner' parameter from the camera
                cam_owner = self.getOwner(cam)

                if cam_owner.strip() == owner:
                    # if it is in the correct owner, return the controller instance
                    self.port = port
                    return cam
                else:
                    # otherwise try to nicely exit the controller
                    gp.check_result(gp.gp_camera_exit(cam))

        # return None if no cameras were found
        return None

    def getOwner(self, camera):
        """getOwner
        get the 'owner' configuration from the camera itself. This is used to specify
        which physical camera we are controlling

        Args:
            camera (object): Either None, or an instance of the gphoto2 camera class

        Returns:
            owner (str): Either None (if something went wrong) or the owner string from the camera
        """
        if camera is None:
            return None
        else:
            # give it a minute to breathe
            sleep(0.1)

            # get the camera configuration
            context = gp.gp_context_new()
            config = gp.check_result(gp.gp_camera_get_config(camera, context))

            # get the owner parameter in the configuration
            owner = gp.check_result(gp.gp_widget_get_child_by_name(config, "ownername"))

            # return the string of the owner
            return gp.check_result(gp.gp_widget_get_value(owner))

    def takePhoto(self):
        """takePhoto
        Tells the canon to capture and store a photo (At this point does not download the photo onto the computer
        only stores it locally)

        Returns:
            filepath (str): path to the photo on the camera
        """
        if self.controller is None:
            return None
        else:
            # Lock the mutex so other threads cannot access the pause_preview variable
            self.set_pause_preview(True)

            # We want to capture raw format images
            self.setImageFormatRAW()

            # capture a photo and return the filepath on the camera
            file_path = self.controller.capture(gp.GP_CAPTURE_IMAGE)

            # the preview cannot preview if the camera is set to raw format
            self.setImageFormatJPEG()

            # Lock the mutex so other threads cannot access the pause_preview variable
            self.set_pause_preview(False)

            return file_path

    def savePhoto(self, camera_path, local_folder):
        """savePhoto
        Given a path to a folder on the camera, and a local folder path, download the
        image from the camera and save it in the folder

        Args:
            camera_path (object): a gphoto2 path object. representing the path to the file on the canon camera
            local_folder (pathlib path object): the local folder the image should be saved in

        Returns:
            True or None: True if successful, None if the controller is None
        """
        if self.controller is None:
            return None
        else:
            # get full target path with filename
            target = local_folder / (self.camera_name + ".cr3")
            self.set_pause_preview(True)
            # get the camera file location from the camera
            camera_file = self.controller.file_get(
                camera_path.folder, camera_path.name, gp.GP_FILE_TYPE_NORMAL
            )
            self.set_pause_preview(False)
            # save the image to the target location
            camera_file.save(
                str(target)
            )  # CR: Check: can wrap in str() so works on windows
            return True

    def setImageFormatJPEG(self):
        """setImageFormatJPEG
        sets the image format for taking images and previews to JPEG
        """
        # 0 is Large Fine JPEG
        # Check options with 'gphoto2 --get-config /main/imgsettings/imageformat'
        self.setConfig("imageformat", 0)

    def setImageFormatRAW(self):
        """setImageFormatRAW
        sets the image format for taking images and previews to RAW
        """
        # 21 is RAW
        # Check options with 'gphoto2 --get-config /main/imgsettings/imageformat'
        self.setConfig("imageformat", 21)

    def setConfig(self, name, value):
        """setConfig
        Set camera configuration with name 'name' to be value

        Args:
            name (string): name of the configuration to be set. Eg, imageformat
            value (int): the value corresponding to the option on the camera. see gphoto2 --list-all-config for options
        """
        if self.controller is not None:
            config = gp.check_result(gp.gp_camera_get_config(self.controller))
            config_item = gp.check_result(gp.gp_widget_get_child_by_name(config, name))

            value = gp.check_result(gp.gp_widget_get_choice(config_item, value))
            gp.check_result(gp.gp_widget_set_value(config_item, value))
            gp.check_result(gp.gp_camera_set_config(self.controller, config))

    def getPreview(self):
        """getPreview

        Returns:
            image (numpy array): Returns x image if failed, otherwise returns the preview as a numpy array from the camera
        """
        if self.controller is None:
            return self.x

        if self.pause_preview:
            self.mutex.lock()
            self.preview_paused = True
            self.mutex.unlock()
            sleep(0.05)
        else:
            self.mutex.lock()
            self.preview_paused = False
            self.mutex.unlock()
            # required configuration will depend on camera type!
            # get configuration tree
            config = gp.check_result(gp.gp_camera_get_config(self.controller))
            # find the image format config item
            # camera dependent - 'imageformat' is 'imagequality' on some
            OK, image_format = gp.gp_widget_get_child_by_name(config, "imageformat")
            if OK >= gp.GP_OK:
                # get current setting
                value = gp.check_result(gp.gp_widget_get_value(image_format))
                # make sure it's not raw
                if "raw" in value.lower():
                    print("Cannot preview raw images")
                    return 1
            # find the capture size class config item
            # need to set this on my Canon 350d to get preview to work at all
            OK, capture_size_class = gp.gp_widget_get_child_by_name(
                config, "capturesizeclass"
            )
            if OK >= gp.GP_OK:
                # set value
                value = gp.check_result(gp.gp_widget_get_choice(capture_size_class, 2))
                gp.check_result(gp.gp_widget_set_value(capture_size_class, value))
                # set config
                gp.check_result(gp.gp_camera_set_config(self.controller, config))
            # capture preview image (not saved to camera memory card)
            camera_file = gp.check_result(gp.gp_camera_capture_preview(self.controller))
            file_data = gp.check_result(gp.gp_file_get_data_and_size(camera_file))
            # display image
            # data = memoryview(file_data)
            image = ImageQt(Image.open(io.BytesIO(file_data)))
            return image
