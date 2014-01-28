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
        self.treeMenu.setColumnCount(5)
        self.treeMenu.setHeaderLabels(["Label", "Type", "Action", "Execute", "ID"])
        self.treeMenu.setSortingEnabled(False)
        self.treeMenu.setAlternatingRowColors(True)
        self.treeMenu.setColumnWidth(0, 150)

        menuFile = self.getBaseMenuFile()

        if menuFile:

            self.obMenu = ObMenu()
            self.obMenu.loadMenu(menuFile)

            rootMenuData = self.obMenu.getMenu(None)
            rootMenuID = rootMenuData[0]["id"]

            # tree root
            self.rootTree = QtGui.QTreeWidgetItem(self.treeMenu)
            self.rootTree.setText(0, rootMenuData[0]["label"])
            self.rootTree.setText(1, rootMenuData[0]["type"])

            # children items
            self.loadMenu(rootMenuID, self.rootTree)

            self.rootTree.setExpanded(True)

            # signal connections
            self.connectSignals()


    def loadMenu(self, parentID, parentItem):
        """
        Loads given menu on QTreeWidget
        """
        menuData = self.obMenu.getMenu(parentID)

        if menuData:
            for it in menuData:

                child = QtGui.QTreeWidgetItem(parentItem)

                if it.has_key("label"):    
                    child.setText(0, it["label"])
                if it.has_key("type"):
                    child.setText(1, it["type"])
                if it.has_key("action"):
                    child.setText(2, it["action"])
                if it.has_key("execute"):                
                    child.setText(3, it["execute"])
                if it.has_key("id"):
                    child.setText(4, it["id"])


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


    def connectSignals(self):
        """
        Connect internal widget signals
        """
        self.treeMenu.itemPressed.connect(self.loadItem)
        

    def loadItem(self, item, column):
        """
        Item pressed slot (loads an item on controls to edit)
        """
        # print "item pressed= column: %s item: %s" % (column, item.text(0))
        self.txtLabel.setText(item.text(0))
        self.txtID.setText(item.text(4))
        #self.txtAction.text(item.text(2))
        self.txtExecute.setText(item.text(3))