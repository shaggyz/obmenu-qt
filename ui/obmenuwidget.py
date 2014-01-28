# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from ui.obmenu import Ui_frmObmenu
from obxml import ObMenu
import os

class ObMenuWidget(Ui_frmObmenu, QtGui.QWidget):
    """
    QtCreator generated file overload
    """
    def __init__(self):
        """
        Constructs the main window
        """
        super(QtGui.QWidget, self).__init__()
        
        self.setupUi(self)
        self.initTree()


    def initTree(self):
        """
        Configures the tree initial state
        """
        self.treeMenu.setColumnCount(4)
        self.treeMenu.setHeaderLabels(["Label", "Type", "Action", "Execute"])
        self.treeMenu.setSortingEnabled(False)
        self.treeMenu.setAlternatingRowColors(True)

        menuFile = self.getBaseMenuFile()

        if menuFile:

            # tree root
            self.rootTree = QtGui.QTreeWidgetItem(self.treeMenu)
            self.rootTree.setText(0, "Openbox 3")
            self.rootTree.setText(1, "menu")

            self.obMenu = ObMenu()
            self.obMenu.loadMenu(menuFile)

            rootMenuData = self.obMenu.getMenu(None)
            rootMenuID = rootMenuData[0]["id"]

            # children items
            self.loadMenu(rootMenuID, self.rootTree)

            self.rootTree.setExpanded(True)


    def loadMenu(self, parentID, parentItem):
        """
        Loads given menu on QTreeWidget
        """
        menuData = self.obMenu.getMenu(parentID)

        if menuData:
            for it in menuData:

                child = QtGui.QTreeWidgetItem(parentItem)
                
                if it["type"] == "item":
                    child.setText(0, it["label"])
                    child.setText(1, "item")
                    child.setText(2, it["action"])
                    child.setText(3, it["execute"])
                elif it["type"] == "separator":
                    child.setText(1, "separator")
                elif it["type"] == "menu":
                    child.setText(0, it["label"])
                    child.setText(1, "menu")
                    self.loadMenu(it["id"], child)


    def getBaseMenuFile(self):
        """
        Gets the main openbox menu file
        """
        menu_path = os.getenv("HOME") + "/.config/openbox/menu.xml"

        if not os.path.isfile(menu_path):
            QtGui.QMessageBox.warning(self, 
                "Missing menu file", 
                "You dont seems to have a openbox menu file in the default location: %s" % (menu_path))
            return None

        return menu_path