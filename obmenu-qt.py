#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, argparse
from PyQt4 import QtGui, QtCore
from ui.main import UiMainWindow
from ui.obmenu import Ui_frmObmenu

class ObMenuQt(object):
    """
    Main program static bootstrap
    """
    
    def __init__(self):
        """
        Initial configuration
        """
        # argument parser
        parser = argparse.ArgumentParser(prog="obmenu-qt",
                                         description="Openbox menu editor based on QT4",
                                         epilog="For more info visit: https://github.com/shaggyz/obmenu-qt",
                                         version="0.01b")
        
        # arguments
        # parser.add_argument("-i", "--ip", help="Listen on this ip")
        # parser.add_argument("-p", "--port", help="Listen on this port")
        # parser.add_argument("-d", "--debug", help="Sets debug mode on", action="store_true")
        
        # arguments = parser.parse_args()

        # if arguments.ip:
        #     environment.setValue("ip", arguments.ip)
        # if arguments.port:
        #     environment.setValue("port", arguments.port)
        # if arguments.debug:
        #     environment.setValue("debug", True)
        
    def start(self):
        """
        Starts the main window
        """
        QTApp = QtGui.QApplication(sys.argv)
        
        mainWindow = UiMainWindow()

        frmMenu = Ui_frmObmenu()
        frmMenu.setupUi(frmMenu)
        frmMenu.show()

        mainWindow.setCentralWidget(frmMenu)

        mainWindow.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        mainWindow.show()

        sys.exit(QTApp.exec_())


"""
Static application entry poiny
"""
if __name__ == "__main__":
    app = ObMenuQt()
    app.start()