from guis.basicGUI import basicGUI
from guis.canonsGUI import canonsGUI
from guis.piEyedPiperGUI import piEyedPiperGUI
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import * 

class SettingCameraDisplayBox(basicGUI):

        def __init__(self, **kwargs):
            super(SettingCameraDisplayBox, self).__init__(**kwargs)
            
            
            setattr(SettingCameraDisplayBox, "colorStatus", "blue")
            setattr(SettingCameraDisplayBox, "grid", self.grid)

            setattr(SettingCameraDisplayBox, "cameras", ["pieye-ant.local", "pieye-beetle.local", "pieye-cicada.local", "pieye-dragonfly.local", "pieye-earwig.local"])

            setattr(SettingCameraDisplayBox, "canons", ["Top", "Side"])

            self.initUI()

        def initUI(self):
            
            i = 0
            #for camera in self.cameras:
            for cam in self.cameras:     
                
                setattr(SettingCameraDisplayBox, f"{cam}", QtWidgets.QLabel())
                
                getattr(SettingCameraDisplayBox, cam).setMaximumWidth(9)
                getattr(SettingCameraDisplayBox, cam).setMaximumHeight(9)

                getattr(SettingCameraDisplayBox, cam).setStyleSheet(f"border: 2px solid {SettingCameraDisplayBox.colorStatus}; background-color: {SettingCameraDisplayBox.colorStatus}; border-radius: 1px;")
                
                SettingCameraDisplayBox.grid.addWidget(getattr(SettingCameraDisplayBox, cam), 0, i, 0, 1, QtCore.Qt.AlignLeft)

                i += 1

                self.setLayout(SettingCameraDisplayBox.grid)



        def updateBox(self, colorStatus, cameraName):

               
            if colorStatus == False:
                getattr(SettingCameraDisplayBox, cameraName).setStyleSheet(f"border: 2px solid red; background-color: red; border-radius: 1px;")
            elif colorStatus == True:
                getattr(SettingCameraDisplayBox, cameraName).setStyleSheet(f"border: 2px solid green; background-color: green; border-radius: 1px;")

            SettingCameraDisplayBox.grid.update()
            
            