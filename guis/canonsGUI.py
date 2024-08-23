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

        self.topCanonGUI = canonGUI("Top", **kwargs)
        self.sideCanonGUI = canonGUI("Side", **kwargs)
        #self.dassco0218GUI = canonGUI("dassco0218", **kwargs)
        self.dassco0024GUI = canonGUI("dassco0024", **kwargs)
        #self.dassco0056GUI = canonGUI("dassco0056", **kwargs)
        #self.dassco0063GUI = canonGUI("dassco0063", **kwargs)
        #self.dassco0215GUI = canonGUI("dassco0215", **kwargs)

        self.reinitCamerasButton = QtWidgets.QPushButton(
            "Reinitialize Canons"
        )
        self.reinitCamerasButton.clicked.connect(self.reinitCameras)
        self.reinitCamerasButton.setStyleSheet("background-color: #d6e6ff;")

        self.reinitTopCameraButton = QtWidgets.QPushButton(
            "Top"
        )
        self.reinitTopCameraButton.clicked.connect(self.reinitTopCamera)
        self.reinitTopCameraButton.setStyleSheet("background-color: #d6e6ff;")

        self.reinitSideCameraButton = QtWidgets.QPushButton(
            "Side"
        )
        self.reinitSideCameraButton.clicked.connect(self.reinitSideCamera)
        self.reinitSideCameraButton.setStyleSheet("background-color: #d6e6ff;")

        #self.reinit218CameraButton = QtWidgets.QPushButton("218")
        #self.reinit218CameraButton.clicked.connect(self.reinit218Camera)
        #self.reinit218CameraButton.setStyleSheet("background-color: #d6e6ff;")

        self.reinit24CameraButton = QtWidgets.QPushButton(
            "24"
        )
        self.reinit24CameraButton.clicked.connect(self.reinit24Camera)
        self.reinit24CameraButton.setStyleSheet("background-color: #d6e6ff;")

        #self.reinit56CameraButton = QtWidgets.QPushButton("56")
        #self.reinit56CameraButton.clicked.connect(self.reinit56Camera)
        #self.reinit56CameraButton.setStyleSheet("background-color: #d6e6ff;")

        #self.reinit63CameraButton = QtWidgets.QPushButton("63")
        #self.reinit63CameraButton.clicked.connect(self.reinit63Camera)
        #self.reinit63CameraButton.setStyleSheet("background-color: #d6e6ff;")

        #self.reinit215CameraButton = QtWidgets.QPushButton("215")
        #self.reinit215CameraButton.clicked.connect(self.reinit215Camera)
        #self.reinit215CameraButton.setStyleSheet("background-color: #d6e6ff;")

        self.initUI()

    def initUI(self):
        #(widget, row, column, row span, column span)
        #self.grid.addWidget(self.inst_title, 0, 1, 1, 1)

        self.grid.addWidget(self.reinitCamerasButton, 0, 1, 1, 1, alignment=QtCore.Qt.AlignLeft)
        self.grid.addWidget(self.reinitTopCameraButton, 0, 3, 1, 1, alignment=QtCore.Qt.AlignLeft)
        self.grid.addWidget(self.reinitSideCameraButton, 0, 5, 1, 1, alignment=QtCore.Qt.AlignLeft)
        #self.grid.addWidget(self.reinit218CameraButton, 0, 12, 1, 1, alignment=QtCore.Qt.AlignLeft)
        self.grid.addWidget(self.reinit24CameraButton, 0, 7, 1, 1, alignment=QtCore.Qt.AlignLeft)
        #self.grid.addWidget(self.reinit56CameraButton, 0, 14, 1, 1, alignment=QtCore.Qt.AlignLeft)
        #self.grid.addWidget(self.reinit63CameraButton, 0, 15, 1, 1, alignment=QtCore.Qt.AlignLeft)
        #self.grid.addWidget(self.reinit215CameraButton, 0, 16, 1, 1, alignment=QtCore.Qt.AlignLeft)
        
        """
        for i in range(16):
            
            if i == 1:
                self.grid.setColumnMinimumWidth(i, 150)
            if i in [2, 3, 4, 12, 13, 14, 15]:
                self.grid.setColumnMinimumWidth(i, 70)
        """

        self.setLayout(self.grid)  
        self.grid.addWidget(self.topCanonGUI, 1, 1, 1, 6)
        self.grid.addWidget(self.sideCanonGUI, 1, 12, 1, 6)
        #self.grid.addWidget(self.dassco0063GUI, 1, 23, 1, 6)
        #self.grid.addWidget(self.dassco0218GUI, 2, 1, 1, 6)
        self.grid.addWidget(self.dassco0024GUI, 1, 23, 1, 6)
        #self.grid.addWidget(self.dassco0056GUI, 2, 23, 1, 6)
        #self.grid.addWidget(self.dassco0215GUI, 2, 34, 1, 6)
        self.setLayout(self.grid)

    def getCameras(self):
        """getCameras
        used by takePhotosGUI to get a list of all the cameras

        Returns:
            cameras [list]: Cameras is a list of the two canonGUI
                camera classes. One for the top camera, and one for the
                side camera
        """
        cameras = [self.topCanonGUI, self.sideCanonGUI, self.dassco0024GUI] # self.dassco0218GUI, self.dassco0024GUI, self.dassco0056GUI, self.dassco0063GUI, self.dassco0215GUI]
        return cameras

    def reinitCameras(self):
        """reinitCameras
        In case there is an issue connecting to the cameras,
           this function attempts to reconnect to all cameras
        """
        self.topCanonGUI.reinitCamera()
        self.sideCanonGUI.reinitCamera()
        #self.dassco0218GUI.reinitCamera()
        self.dassco0024GUI.reinitCamera()
        #self.dassco0056GUI.reinitCamera()
        #self.dassco0063GUI.reinitCamera()
        #self.dassco0215GUI.reinitCamera()

    def reinitTopCamera(self):
        self.topCanonGUI.reinitCamera()
    
    def reinitSideCamera(self):
        self.sideCanonGUI.reinitCamera()

    def reinit218Camera(self):
        self.dassco0218GUI.reinitCamera()

    def reinit24Camera(self):
        self.dassco0024GUI.reinitCamera()

    def reinit56Camera(self):
        self.dassco0056GUI.reinitCamera()

    def reinit63Camera(self):
        self.dassco0063GUI.reinitCamera()

    def reinit215Camera(self):
        self.dassco0215GUI.reinitCamera()