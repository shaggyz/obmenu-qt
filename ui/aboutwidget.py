# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from ui.about import Ui_frmAbout
import os

class ObAboutWidget(Ui_frmAbout, QtGui.QWidget):
    """
    About widget container
    """
    def __init__(self):
        """
        Constructs the about window
        """
        super(QtGui.QWidget, self).__init__()

        self.setupUi(self)

        self.iconPath = os.getcwd() + "/icons/"
        self.setWindowTitle("Openbox menu configuration - About")
        self.setWindowIcon(QtGui.QIcon(self.iconPath + "mnu48.png"))

