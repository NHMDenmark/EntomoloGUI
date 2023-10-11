from guis.basicGUI import basicGUI
from guis.canonsGUI import canonsGUI
from guis.piEyedPiperGUI import piEyedPiperGUI
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import * 

class SettingCameraDisplayBox(basicGUI):

        def __init__(self, **kwargs):
            super(SettingCameraDisplayBox, self).__init__(**kwargs)
            
            
            setattr(SettingCameraDisplayBox, "colorStatus", "#43b0f1")
            setattr(SettingCameraDisplayBox, "grid", self.grid)

            setattr(SettingCameraDisplayBox, "cameras", ["pieye-ant.local", "pieye-beetle.local", "pieye-cicada.local", "pieye-dragonfly.local", "pieye-earwig.local"])

            setattr(SettingCameraDisplayBox, "canons", ["Top", "Side"])

            self.initUI()

        def initUI(self):
            
            i = 0
            #for camera in self.cameras:
            for cam in self.cameras:     
                name = f"{cam}"[6:-6]
                label = QtWidgets.QLabel(name)
                setattr(SettingCameraDisplayBox, f"{cam}", QtWidgets.QLabel())
                
                getattr(SettingCameraDisplayBox, cam).setMaximumWidth(11)
                getattr(SettingCameraDisplayBox, cam).setMaximumHeight(11)

                getattr(SettingCameraDisplayBox, cam).setStyleSheet(f"border: 2px solid {SettingCameraDisplayBox.colorStatus}; background-color: {SettingCameraDisplayBox.colorStatus}; border-radius: 1px;")
                

                SettingCameraDisplayBox.grid.addWidget(label, i, 0, 1, 1, QtCore.Qt.AlignRight)
                SettingCameraDisplayBox.grid.addWidget(getattr(SettingCameraDisplayBox, cam), i, 1, 1, 1, QtCore.Qt.AlignLeft)

                i += 1

                self.setLayout(SettingCameraDisplayBox.grid)

            t = 0

            for cam in self.canons:     
                
                label = QtWidgets.QLabel(f"{cam}")

                setattr(SettingCameraDisplayBox, f"{cam}", QtWidgets.QLabel())
                
                getattr(SettingCameraDisplayBox, cam).setMaximumWidth(11)
                getattr(SettingCameraDisplayBox, cam).setMaximumHeight(11)

                getattr(SettingCameraDisplayBox, cam).setStyleSheet(f"border: 2px solid {SettingCameraDisplayBox.colorStatus}; background-color: {SettingCameraDisplayBox.colorStatus}; border-radius: 1px;")
                

                SettingCameraDisplayBox.grid.addWidget(label, t + 5, 0, 1, 1, QtCore.Qt.AlignRight)
                SettingCameraDisplayBox.grid.addWidget(getattr(SettingCameraDisplayBox, cam), t + 5, 1, 1, 1, QtCore.Qt.AlignLeft)

                t += 1

                self.setLayout(SettingCameraDisplayBox.grid)
                print(cam)



        def updateBox(self, colorStatus, cameraName):

               
            if colorStatus == False:
                getattr(SettingCameraDisplayBox, cameraName).setStyleSheet(f"border: 2px solid #b8e0d4; background-color: #b8e0d4; border-radius: 1px;")
            elif colorStatus == True:
                getattr(SettingCameraDisplayBox, cameraName).setStyleSheet(f"border: 2px solid #43b0f1; background-color: #43b0f1; border-radius: 1px;")

            SettingCameraDisplayBox.grid.update()
            
            