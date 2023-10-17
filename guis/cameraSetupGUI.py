from guis.basicGUI import basicGUI
from guis.cameraSettingBoxGUI import SettingCameraDisplayBox
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import * 
import json

"""
    Includes the classes CameraSetupGUI, SettingChooser and JsonCameraSetting
"""

class CameraSetupGUI(basicGUI):
    """
    Controls and takes care of creating and deleting camera settings.
    """
    def __init__(self, **kwargs):
        super(CameraSetupGUI, self).__init__(**kwargs)
        
        self.sc = SettingChooser()
        self.js = self.sc.js
        self.initUI()
    
    def initUI(self):
        
        self.chooseCamerasButton = QtWidgets.QPushButton("Settings")
        self.chooseCamerasButton.clicked.connect(self.msg_box_checked_cameras)
        self.chooseCamerasButton.setStyleSheet("background-color: #d6e6ff;")
        self.grid.addWidget(self.chooseCamerasButton)

        self.setLayout(self.grid)
        

    def msg_box_checked_cameras(self):
        """
        Menu message box for creating or deleting camera settings.
        """
        self.dialogBox = QDialog()
        self.dialogLayout = QVBoxLayout()
        self.dialogBox.setLayout(self.dialogLayout)
        
        deleteButton = self.button_creator("Delete setting", self.delete_action)
        self.dialogLayout.addWidget(deleteButton)

        createButton = self.button_creator("New setting", self.create_action)
        self.dialogLayout.addWidget(createButton)

        cancelButton = self.button_creator("Cancel", self.cancel_action)
        self.dialogLayout.addWidget(cancelButton)

        self.dialogBox.resize(200, 200)

        self.dialogBox.exec_()


    def button_creator(self, text, action):
        """
        Creates new buttons for message boxes
        """
        button = QPushButton(text)
        button.clicked.connect(action)
        return button

    def cancel_action_delete(self):
        # closes and cancels a messagebox
        self.dialogBoxDelete.close()
    
    def cancel_action_create(self):
        # closes and cancels a messagebox
        self.dialogBoxCreate.close()
    
    def cancel_action(self):
        # closes and cancels a messagebox
        self.dialogBox.close()
        
    def create_action(self):
        """
        Brings up a messagebox that allows the creation of a new menu setting. Uses checkboxes and a written input field. 
        """

        # closes the previous messagebox
        self.dialogBox.close()

        # creates a new messagebox with options for camera settings
        self.dialogBoxCreate = QDialog()
        self.dialogLayoutCreate = QVBoxLayout()
        self.dialogBoxCreate.setLayout(self.dialogLayoutCreate)

        self.labelCreateCameras = QtWidgets.QLabel("Add cameras to new setting:")
        self.dialogLayoutCreate.addWidget(self.labelCreateCameras)

        self.checkAnt = QCheckBox("pieye-ant")
        self.dialogLayoutCreate.addWidget(self.checkAnt)
        self.checkBeetle = QCheckBox("pieye-beetle")
        self.dialogLayoutCreate.addWidget(self.checkBeetle)
        self.checkCicada = QCheckBox("pieye-cicada")
        self.dialogLayoutCreate.addWidget(self.checkCicada)
        self.checkDragonfly = QCheckBox("pieye-dragonfly")
        self.dialogLayoutCreate.addWidget(self.checkDragonfly)
        self.checkEarwig = QCheckBox("pieye-earwig")
        self.dialogLayoutCreate.addWidget(self.checkEarwig)
        self.checkTop = QCheckBox("Canon Top")
        self.dialogLayoutCreate.addWidget(self.checkTop)
        self.checkSide = QCheckBox("Canon Side")
        self.dialogLayoutCreate.addWidget(self.checkSide)

        self.inputName = QLineEdit()
        self.inputName.setPlaceholderText("Choose a name for the new setting")
        self.inputName.setMaxLength(20)
        self.dialogLayoutCreate.addWidget(self.inputName)

        createButton = self.button_creator("Add new setting", self.create_setting)
        self.dialogLayoutCreate.addWidget(createButton)

        cancelButton = self.button_creator("Cancel", self.cancel_action_create)
        self.dialogLayoutCreate.addWidget(cancelButton)

        self.dialogBoxCreate.resize(300, 200)
        self.dialogBoxCreate.exec_()

    def create_setting(self):
        """
        Checks and handles that a new setting has a name. Creates the new setting. 
        A new setting is sent to JsonCameraSetting for saving in the json file.
        Updates the Setting chooser with the new setting.  
        """
        self.dialogBoxCreate.close()

        # checks for name input
        if self.inputName.text() != "":
            
            # creates new setting
            self.newSetting = {
                self.inputName.text(): {
                "pieye-ant.local": self.checkAnt.isChecked(),
                "pieye-beetle.local": self.checkBeetle.isChecked(),
                "pieye-cicada.local": self.checkCicada.isChecked(),
                "pieye-dragonfly.local": self.checkDragonfly.isChecked(),
                "pieye-earwig.local": self.checkEarwig.isChecked(),
                "Top": self.checkTop.isChecked(),
                "Side": self.checkSide.isChecked()
                }
                }
            # adds setting to existing settings
            self.js.settings.update(self.newSetting)
            # updates JsonCameraSettings to include new setting
            self.js.update_json_camera_settings(self.js.settings)
            # updates Setting chooser to include new setting
            self.sc.update_setting_chooser()

            # UI information for user that their setting was created or not 
            self.acceptCreateMsgBox = QMessageBox()

            self.acceptCreateMsgBox.setText("New setting created")
            self.acceptCreateMsgBox.addButton(QMessageBox.Ok)

            self.acceptCreateMsgBox.exec_()
        elif self.inputName.text() == "":

            self.acceptCreateMsgBox = QMessageBox()

            self.acceptCreateMsgBox.setText("Setting name is required")
            self.acceptCreateMsgBox.addButton(QMessageBox.Ok)

            self.acceptCreateMsgBox.exec_()

    def delete_action(self):
        """
        Creates dialog box with current settings. Allows user to choose one and delete it.
        Ensures the default setting with all cameras active cant be deleted. 
        Tells JsonCameraSetting to update the json file.
        Updates the Setting chooser afterward.  
        """
        #close old box
        self.dialogBox.close()
        #create delete box ui
        self.dialogBoxDelete = QDialog()
        self.dialogLayoutDelete = QVBoxLayout()
        self.dialogBoxDelete.setLayout(self.dialogLayoutDelete)

        self.label = QtWidgets.QLabel("Choose a setting to delete:")
        self.comboboxDelete = QComboBox()
        self.comboboxDelete.setStyleSheet("background-color: #d6e6ff; min-width: 120px;")
        
        self.dialogLayoutDelete.addWidget(self.label)
        
        self.settingsDelete = self.js.settings

        for setting in self.settingsDelete:
            self.comboboxDelete.addItem(setting)
        # takes away the default setting so it cant be removed
        self.comboboxDelete.removeItem(0)
        # adds 1 to the chosen setting index to account for removing the default setting
        setattr(CameraSetupGUI ,"indexToBeDeleted", (self.comboboxDelete.currentIndex() + 1))

        # updates setting index when user points at a different setting
        self.comboboxDelete.currentIndexChanged.connect(lambda index: self.set_index_to_be_deleted(index))

        self.dialogLayoutDelete.addWidget(self.comboboxDelete)

        self.labelEmpty = QtWidgets.QLabel()
        self.dialogLayoutDelete.addWidget(self.labelEmpty)

        # button that deletes the chosen setting
        createButton = self.button_creator("Delete setting", self.delete_setting)
        self.dialogLayoutDelete.addWidget(createButton)

        cancelButton = self.button_creator("Cancel", self.cancel_action_delete)
        self.dialogLayoutDelete.addWidget(cancelButton)

        self.dialogBoxDelete.resize(200, 200)

        self.dialogBoxDelete.exec_()

    def set_index_to_be_deleted(self, index):
        # updates the chosen index of the user. +1 to account for default setting being excluded.
        setattr(CameraSetupGUI ,"indexToBeDeleted", (index + 1))

    def delete_setting(self):
        """
        Activates through the delete button.
        Tells JsonCameraSetting to delete the chosen setting.
        Updates the SettingChooser and ends the dialog.  
        """
        self.js.delete_setting(getattr(self, "indexToBeDeleted"))

        self.sc.update_setting_chooser()
        self.dialogBoxDelete.close()

class SettingChooser(basicGUI):
    """
    Creates and controls a combobox(dropdown scroll menu),
    that allows users to choose which camera setting they want to use.
    """
    def __init__(self, **kwargs):
        super(SettingChooser, self).__init__(**kwargs)
        
        self.js = JsonCameraSetting()
        
        box = QComboBox()
        setattr(SettingChooser, "grid", self.grid)
        setattr(SettingChooser, "combobox", box)

        self.initUI()
    
    def initUI(self):

        self.label = QtWidgets.QLabel("Camera setup options:")

        getattr(self, "combobox").setStyleSheet("background-color: #d6e6ff; min-width: 190px;")
        
        self.settings = self.js.settings

        for setting in self.settings:
            getattr(self, "combobox").addItem(setting)
        
        startIndex = getattr(self, "combobox").currentIndex()
        self.js.set_current_setting(startIndex)

        # changes current index whenever a setting has been chosen
        SettingChooser.combobox.currentIndexChanged.connect(lambda index: self.js.set_current_setting(index))

        SettingChooser.grid.addWidget(getattr(self, "combobox"))

        self.setLayout(getattr(self, "grid"))

    def update_setting_chooser(self):
        """
        Deletes old combobox and creates a new one effectively updating,
        whenever changes to the list of settings has taken place.
        Sets default setting as the chosen setting after each reset.
        """
        # removes old combobox
        SettingChooser.grid.removeWidget(SettingChooser.combobox)

        # builds a new box
        box = QComboBox()
        setattr(SettingChooser, "combobox", box)
        getattr(self, "combobox").setStyleSheet("background-color: #d6e6ff;")

        self.settings = self.js.settings

        for setting in self.settings:
            getattr(self, "combobox").addItem(setting)

        SettingChooser.combobox.currentIndexChanged.connect(lambda index: self.js.set_current_setting(index))

        SettingChooser.grid.addWidget(getattr(self, "combobox"))

        # refreshes the grid holding the combobox
        SettingChooser.grid.update()
        # sets default setting as chosen setting
        self.js.set_current_setting(0)

class JsonCameraSetting(basicGUI):
    """
    Handles updates to the camera_setting.json file. Keeps track of current camera setting.
    """
    def __init__(self, **kwargs):
        super(JsonCameraSetting, self).__init__(**kwargs)

        self.settings = []

        with open("./camera_settings.json", "r") as f:
            self.settings = json.load(f)

        self.scdb = SettingCameraDisplayBox()
        
        self.set_current_setting()
        

    def update_json_camera_settings(self, dicts):
        """
        Takes an updated list and overwrites the json file. 
        """
        with open("./camera_settings.json", "w") as f:
            json.dump(dicts, f)
    
    def set_current_setting(self, index = 0):
        """
        Updates current setting. Sets default setting as current setting if needed.
        Asks cameraSettingBoxGUI to update the camera chosen box area with current setting.
        """
        # Convert the keys into a list
        keys_list = list(self.settings.keys())
        
        key = keys_list[index]

        setattr(JsonCameraSetting, "currentSetting", self.settings[key])   

        for cam in self.scdb.cameras:
            setting = self.currentSetting[cam]

            self.scdb.updateBox(colorStatus=setting, cameraName=cam)

        for cam in self.scdb.canons:
            setting = self.currentSetting[cam]
            
            self.scdb.updateBox(colorStatus=setting, cameraName=cam)

    def delete_setting(self, index_to_delete):
        """
        Takes a index number and deletes the corresponding setting. 
        """

        keys_list = list(self.settings.keys())
    
        if 0 <= index_to_delete < len(keys_list):
            key_to_delete = keys_list[index_to_delete]
            del self.settings[key_to_delete]
            self.update_json_camera_settings(self.settings)
            print(f"Setting at index {index_to_delete} deleted.")
        else:
            print(f"Invalid index: {index_to_delete}")

         