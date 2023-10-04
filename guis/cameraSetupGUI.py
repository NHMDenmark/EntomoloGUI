from guis.basicGUI import basicGUI
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import * 
import json

class CameraSetupGUI(basicGUI):
    
    def __init__(self, **kwargs):
        super(CameraSetupGUI, self).__init__(**kwargs)
        
        self.initUI()
    
    def initUI(self):
        
        self.chooseCamerasButton = QtWidgets.QPushButton("Choose cameras")
        self.chooseCamerasButton.clicked.connect(self.msg_box_checked_cameras)
        self.chooseCamerasButton.setStyleSheet("background-color: #d6e6ff;")
        self.grid.addWidget(self.chooseCamerasButton)

        self.setLayout(self.grid)
        

    def msg_box_checked_cameras(self):
        
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle("Camera setup menu")
        msg_box.setText("Create or delete a camera setting.")
        
        msg_box.addButton("Cancel", QMessageBox.RejectRole)
        msg_box.addButton("Delete", QMessageBox.AcceptRole)
        msg_box.addButton("New", QMessageBox.YesRole)
        
        msg_box.buttonClicked.connect(self.choice_director)
        msg_box.exec_()

    def choice_director(self, button):
        if button.text() == "Delete":
            self.delete_action()
        if button.text() == "New":
            self.create_action()
    
        
    def create_action(self):
        print("create")
        

    def delete_action(self):







        jc = JsonCameraSetting()

        print(jc.settings.keys())

class SettingChooser(basicGUI):

    def __init__(self, **kwargs):
        super(SettingChooser, self).__init__(**kwargs)
        
        self.initUI()
    
    def initUI(self):

        self.label = QtWidgets.QLabel("Camera setup options:")
        self.combobox = QComboBox()
        self.combobox.setStyleSheet("background-color: #d6e6ff;")
        
        js = JsonCameraSetting()
        self.settings = js.settings

        for setting in self.settings:
            self.combobox.addItem(setting)
        
        self.combobox.currentIndexChanged.connect(lambda index: js.set_current_setting(index))

        self.grid.addWidget(self.combobox)

        self.setLayout(self.grid)

        
        

class JsonCameraSetting(basicGUI):

    def __init__(self):
        
        self.settings = []

        with open("../camera_settings.json", "r") as f:
            self.settings = json.load(f)

        self.currentSetting = self.settings["weird_test_bugs"]    
        

    def update_json_camera_settings(self, dicts):

        with open("../camera_settings.json", "w") as f:
            json.dump(dicts)
    
    def set_current_setting(self, index):
        print(index)
        #self.currentSetting = self.settings[index]   
    