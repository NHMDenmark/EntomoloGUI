#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  2 20:01:42 2018

@author: robertahunt
"""
from PyQt5 import QtWidgets, QtCore

from guis.basicGUI import basicGUI
from guis.canonGUI import canonGUI
from guis.progressDialog import progressDialog


class canonsGUI(basicGUI):
    """
    The GUI for the two canon previews
    """

    def __init__(self, **kwargs):
        super(canonsGUI, self).__init__(**kwargs)
        # self.inst_title = self.headerLabel("Fire the Canons!")

        self.R10CanonGUI = canonGUI("R10", **kwargs)
        self.dassco0024GUI = canonGUI("dassco0024", **kwargs)
        self.dassco0041GUI = canonGUI("dassco0041", **kwargs)
        self.dassco0056GUI = canonGUI("dassco0056", **kwargs)
        self.dassco0042GUI = canonGUI("dassco0042", **kwargs)
        self.dassco0215GUI = canonGUI("dassco0215", **kwargs)

        self.reinitCamerasButton = QtWidgets.QPushButton(
            "Reinitialize Canons"
        )
        self.reinitCamerasButton.clicked.connect(self.reinitCameras)
        self.reinitCamerasButton.setStyleSheet("background-color: #d6e6ff;")


        self.reinitR10CameraButton = QtWidgets.QPushButton(
            "R10"
        )
        self.reinitR10CameraButton.clicked.connect(self.reinitR10Camera)
        self.reinitR10CameraButton.setStyleSheet("background-color: #d6e6ff;")

        self.reinit24CameraButton = QtWidgets.QPushButton(
            "24"
        )
        self.reinit24CameraButton.clicked.connect(self.reinit24Camera)
        self.reinit24CameraButton.setStyleSheet("background-color: #d6e6ff;")

        self.reinit41CameraButton = QtWidgets.QPushButton(
            "41"
        )
        self.reinit41CameraButton.clicked.connect(self.reinit41Camera)
        self.reinit41CameraButton.setStyleSheet("background-color: #d6e6ff;")

        self.reinit56CameraButton = QtWidgets.QPushButton(
            "56"
        )
        self.reinit56CameraButton.clicked.connect(self.reinit56Camera)
        self.reinit56CameraButton.setStyleSheet("background-color: #d6e6ff;")

        self.reinit42CameraButton = QtWidgets.QPushButton(
            "42"
        )
        self.reinit42CameraButton.clicked.connect(self.reinit42Camera)
        self.reinit42CameraButton.setStyleSheet("background-color: #d6e6ff;")

        self.reinit215CameraButton = QtWidgets.QPushButton(
            "215"
        )
        self.reinit215CameraButton.clicked.connect(self.reinit215Camera)
        self.reinit215CameraButton.setStyleSheet("background-color: #d6e6ff;")

        self.initUI()

    def initUI(self):
        #self.grid.addWidget(self.inst_title, 0, 1, 1, 1)

        self.grid.addWidget(self.reinitCamerasButton, 0, 1, 1, 1, alignment=QtCore.Qt.AlignLeft)
        self.grid.addWidget(self.reinitR10CameraButton, 0, 3, 1, 1, alignment=QtCore.Qt.AlignLeft)
        self.grid.addWidget(self.reinit24CameraButton, 0, 12, 1, 1, alignment=QtCore.Qt.AlignLeft)
        self.grid.addWidget(self.reinit41CameraButton, 0, 13, 1, 1, alignment=QtCore.Qt.AlignLeft)
        self.grid.addWidget(self.reinit56CameraButton, 0, 14, 1, 1, alignment=QtCore.Qt.AlignLeft)
        self.grid.addWidget(self.reinit42CameraButton, 0, 15, 1, 1, alignment=QtCore.Qt.AlignLeft)
        self.grid.addWidget(self.reinit215CameraButton, 0, 16, 1, 1, alignment=QtCore.Qt.AlignLeft)
        
        for i in range(16):
            
            if i == 1:
                self.grid.setColumnMinimumWidth(i, 150)
            if i in [2, 3, 4, 12, 13, 14, 15]:
                self.grid.setColumnMinimumWidth(i, 70)
        

        self.setLayout(self.grid)  
        self.grid.addWidget(self.R10CanonGUI, 1, 12, 1, 6)
        self.grid.addWidget(self.dassco0042GUI, 1, 23, 1, 6)
        self.grid.addWidget(self.dassco0024GUI, 1, 1, 1, 6)
        self.grid.addWidget(self.dassco0041GUI, 2, 12, 1, 6)
        self.grid.addWidget(self.dassco0056GUI, 2, 23, 1, 6)
        self.grid.addWidget(self.dassco0215GUI, 2, 1, 1, 6)
        self.setLayout(self.grid)

    def getCameras(self):
        """getCameras
        used by takePhotosGUI to get a list of all the cameras

        Returns:
            cameras [list]: Cameras is a list of the two canonGUI
                camera classes. One for the MARK4 camera, and one for the
                R10 camera
        """
        cameras = [self.R10CanonGUI, self.dassco0024GUI, self.dassco0041GUI, self.dassco0056GUI, self.dassco0042GUI, self.dassco0215GUI]
        return cameras

    def reinitCameras(self):
        """reinitCameras
        In case there is an issue connecting to the cameras,
           this function attempts to reconnect to all cameras
        """
        self.R10CanonGUI.reinitCamera()
        self.dassco0024GUI.reinitCamera()
        self.dassco0041GUI.reinitCamera()
        self.dassco0056GUI.reinitCamera()
        self.dassco0042GUI.reinitCamera()
        self.dassco0215GUI.reinitCamera()

    def reinitR10Camera(self):
        self.R10CanonGUI.reinitCamera()

    def reinit24Camera(self):
        self.dassco0024GUI.reinitCamera()

    def reinit41Camera(self):
        self.dassco0041GUI.reinitCamera()

    def reinit56Camera(self):
        self.dassco0056GUI.reinitCamera()

    def reinit42Camera(self):
        self.dassco0042GUI.reinitCamera()

    def reinit215Camera(self):
        self.dassco0215GUI.reinitCamera()