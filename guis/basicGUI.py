import sys
import logging
import warnings

from PyQt5 import QtGui, QtWidgets, QtCore


class ClickableIMG(QtWidgets.QLabel):
    """ClickableIMG
    Makes a container for an image that can do something when clicked.
    This can be connected with something like: object.clicked.connect(event)

    Args:
        QtWidgets (_type_): _description_
    """

    clicked = QtCore.pyqtSignal(str)

    def mousePressEvent(self, event):
        self.clicked.emit(self.objectName())


class basicGUI(QtWidgets.QWidget):
    """basicGUI
    Adds some basic functionality on top of the normal Widget
    such as logging and a warning popup
    """

    def __init__(self, threadpool=None):
        super(basicGUI, self).__init__()
        self.grid = QtWidgets.QGridLayout()
        self.grid.setSpacing(10)
        self.log = logging.getLogger("UThread")
        self.threadpool = threadpool

    def headerLabel(self, text):
        """headerLabel
        generate a new headerlabel with specific font

        Args:
            text (str): header text

        Returns:
            headerLabel: the header label object
        """
        headerLabel = QtWidgets.QLabel(text)
        headerFont = QtGui.QFont("Times", 20, QtGui.QFont.Bold)
        headerLabel.setFont(headerFont)
        return headerLabel

    def warn(self, msg, _exit=False):
        """warn

        Args:
            msg (str): Message to be displayed explaining the warning
            _exit (bool, optional): Whether to exit the entire application or not after this warning is closed. Defaults to False.
        """
        warnings.warn(msg)
        warning = QtWidgets.QMessageBox()
        warning.setWindowTitle("Warning Encountered")
        warning.setText(msg)
        warning.exec_()
        if _exit:
           sys.exit()
