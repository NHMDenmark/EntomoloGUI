from guis.basicGUI import basicGUI
from guis.cameraSettingBoxGUI import SettingCameraDisplayBox
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import * 
import json

class CameraSetupGUI(basicGUI):
    
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
        button = QPushButton(text)
        button.clicked.connect(action)
        return button

    def cancel_action_delete(self):
        self.dialogBoxDelete.close()
    
    def cancel_action_create(self):
        self.dialogBoxCreate.close()
    
    def cancel_action(self):
        self.dialogBox.close()
        
    def create_action(self):
        self.dialogBox.close()

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
        #self.checkAnt.isChecked()

        self.inputName = QLineEdit()
        self.inputName.setPlaceholderText("Choose a name for the new setting")
        self.dialogLayoutCreate.addWidget(self.inputName)
        #text = self.inputName.text()

        createButton = self.button_creator("Add new setting", self.create_setting)
        self.dialogLayoutCreate.addWidget(createButton)

        cancelButton = self.button_creator("Cancel", self.cancel_action_create)
        self.dialogLayoutCreate.addWidget(cancelButton)

        self.dialogBoxCreate.resize(300, 200)
        self.dialogBoxCreate.exec_()

    def create_setting(self):

        self.dialogBoxCreate.close()

        if self.inputName.text() is not "":
            
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

            self.js.settings.update(self.newSetting)

            self.js.update_json_camera_settings(self.js.settings)

            self.sc.update_setting_chooser()

            self.acceptCreateMsgBox = QMessageBox()

            self.acceptCreateMsgBox.setText("New setting created")
            self.acceptCreateMsgBox.addButton(QMessageBox.Ok)

            self.acceptCreateMsgBox.exec_()
        elif self.inputName.text() is "":

            self.acceptCreateMsgBox = QMessageBox()

            self.acceptCreateMsgBox.setText("Setting name is required")
            self.acceptCreateMsgBox.addButton(QMessageBox.Ok)

            self.acceptCreateMsgBox.exec_()

    def delete_action(self):
        self.dialogBox.close()

        self.dialogBoxDelete = QDialog()
        self.dialogLayoutDelete = QVBoxLayout()
        self.dialogBoxDelete.setLayout(self.dialogLayoutDelete)

        self.label = QtWidgets.QLabel("Choose a setting to delete:")
        self.comboboxDelete = QComboBox()
        self.comboboxDelete.setStyleSheet("background-color: #d6e6ff;")
        
        self.dialogLayoutDelete.addWidget(self.label)
        
        self.settingsDelete = self.js.settings

        for setting in self.settingsDelete:
            self.comboboxDelete.addItem(setting)
        
        self.comboboxDelete.removeItem(0)

        setattr(CameraSetupGUI ,"indexToBeDeleted", (self.comboboxDelete.currentIndex() + 1))

        self.comboboxDelete.currentIndexChanged.connect(lambda index: self.set_index_to_be_deleted(index))

        self.dialogLayoutDelete.addWidget(self.comboboxDelete)

        self.labelEmpty = QtWidgets.QLabel()
        self.dialogLayoutDelete.addWidget(self.labelEmpty)

        createButton = self.button_creator("Delete setting", self.delete_setting)
        self.dialogLayoutDelete.addWidget(createButton)

        cancelButton = self.button_creator("Cancel", self.cancel_action_delete)
        self.dialogLayoutDelete.addWidget(cancelButton)

        self.dialogBoxDelete.resize(200, 200)

        self.dialogBoxDelete.exec_()

    def set_index_to_be_deleted(self, index):
        setattr(CameraSetupGUI ,"indexToBeDeleted", (index + 1))
        print("index:", index +1)

    def delete_setting(self):
        
        self.js.delete_setting(getattr(self, "indexToBeDeleted"))

        self.sc.update_setting_chooser()
        self.dialogBoxDelete.close()

class SettingChooser(basicGUI):

    def __init__(self, **kwargs):
        super(SettingChooser, self).__init__(**kwargs)
        
        self.js = JsonCameraSetting()
        
        box = QComboBox()
        setattr(SettingChooser, "grid", self.grid)
        setattr(SettingChooser, "combobox", box)

        self.initUI()
    
    def initUI(self):

        self.label = QtWidgets.QLabel("Camera setup options:")
        # self.combobox = QComboBox()
        getattr(self, "combobox").setStyleSheet("background-color: #d6e6ff;")
        
        
        self.settings = self.js.settings

        for setting in self.settings:
            getattr(self, "combobox").addItem(setting)
        
        startIndex = getattr(self, "combobox").currentIndex()
        self.js.set_current_setting(startIndex)

        SettingChooser.combobox.currentIndexChanged.connect(lambda index: self.js.set_current_setting(index))

        SettingChooser.grid.addWidget(getattr(self, "combobox"))

        self.setLayout(getattr(self, "grid"))

    def update_setting_chooser(self):
        
        SettingChooser.grid.removeWidget(SettingChooser.combobox)
        box = QComboBox()
        setattr(SettingChooser, "combobox", box)
        getattr(self, "combobox").setStyleSheet("background-color: #d6e6ff;")

        self.settings = self.js.settings

        for setting in self.settings:
            getattr(self, "combobox").addItem(setting)

        SettingChooser.combobox.currentIndexChanged.connect(lambda index: self.js.set_current_setting(index))

        SettingChooser.grid.addWidget(getattr(self, "combobox"))

        SettingChooser.grid.update()
        self.js.set_current_setting(0)

class JsonCameraSetting(basicGUI):

    def __init__(self, **kwargs):
        super(JsonCameraSetting, self).__init__(**kwargs)
        print("json init")

        self.settings = []

        with open("./camera_settings.json", "r") as f:
            self.settings = json.load(f)
            

        self.scdb = SettingCameraDisplayBox()
        
        self.set_current_setting()
        

    def update_json_camera_settings(self, dicts):

        with open("./camera_settings.json", "w") as f:
            json.dump(dicts, f)
    
    def set_current_setting(self, index = 0):

        # Convert the keys into a list
        keys_list = list(self.settings.keys())
        
        key = keys_list[index]

        setattr(JsonCameraSetting, "currentSetting", self.settings[key])   

        for cam in self.scdb.cameras:
            setting = self.currentSetting[cam]

            print(setting, cam)
            self.scdb.updateBox(colorStatus=setting, cameraName=cam)

        #print(self.currentSetting)

    def delete_setting(self, index_to_delete):
        keys_list = list(self.settings.keys())
    
        if 0 <= index_to_delete < len(keys_list):
            key_to_delete = keys_list[index_to_delete]
            del self.settings[key_to_delete]
            self.update_json_camera_settings(self.settings)
            print(f"Setting at index {index_to_delete} deleted.")
        else:
            print(f"Invalid index: {index_to_delete}")

         