#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import argparse
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QStyle

from .ui.main import UiMainWindow

class ObMenuQt(object):
    """
    Main program static bootstrap
    """
    VERSION = "1.0"
    
    def __init__(self):
        """
        Initial configuration
        """
        self.file = None

        # argument parser
        parser = argparse.ArgumentParser(prog="obmenu-qt",
                                         description="Openbox menu editor based on QT4",
                                         epilog="For more info visit: https://github.com/shaggyz/obmenu-qt",
                                         version=self.VERSION)
        
        # arguments
        parser.add_argument("-f", "--file", help="Load this menu file on start")
        arguments = parser.parse_args()

        if arguments.file:
             self.file = arguments.file

    def start(self):
        """
        Starts the main window
        """
        QTApp = QtGui.QApplication(sys.argv)

        app_dir = os.path.dirname(os.path.realpath(__file__))
        icon_dir = app_dir + os.path.sep + "icons" + os.path.sep

        mainWindow = UiMainWindow(self.VERSION, icon_path=icon_dir)
        mainWindow.setGeometry(
            QStyle.alignedRect(
                QtCore.Qt.LeftToRight,
                QtCore.Qt.AlignCenter,
                mainWindow.size(),
                QTApp.desktop().availableGeometry()))

        mainWindow.show()

        sys.exit(QTApp.exec_())

def main():
    app = ObMenuQt()
    app.start()


"""
Static application entry poiny
"""
if __name__ == "__main__":
    main()