from PyQt5 import QtGui, QtWidgets
import os

from ob_menu_qt.ui.about import Ui_frmAbout


class ObAboutWidget(Ui_frmAbout, QtWidgets.QDialog):
    """
    About widget container
    """
    def __init__(self, icon_path):
        """
        Constructs the about window
        """
        super(QtWidgets.QDialog, self).__init__()

        self.setupUi(self)
        self.icon_path = icon_path

        self.setWindowTitle("Openbox menu configuration - About")
        self.setWindowIcon(QtGui.QIcon(self.icon_path + "mnu48.png"))

    def set_version(self, version):
        """
        Sets the program version
        """
        self.lblVersion.setText(version)
