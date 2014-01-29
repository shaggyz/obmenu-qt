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

        # Combo options
        actions = []
        actions.append("Execute")
        actions.append("Reconfigure")
        actions.append("Restart")
        actions.append("Exit")
        self.cmbAction.addItems(actions)
        self.cmbAction.setDisabled(True)

        self.changed = False


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
        self.txtExecute.textEdited.connect(self.updateExecute)


    def loadItem(self, item, column):
        """
        Item pressed slot (loads an item on controls to edit)
        """
        # print self.treeMenu.currentIndex().row()

        self.txtLabel.setText(item.text(0))
        self.txtID.setText(item.text(4))
        
        selIndex = self.cmbAction.findText(item.text(2))
        
        if selIndex is -1:
            self.cmbAction.setDisabled(True)
        else:
            self.cmbAction.setDisabled(False)
            self.cmbAction.setCurrentIndex(selIndex)

        self.txtExecute.setText(item.text(3))


    def reconfigureOpenbox(self):
        """
        Kills the openbox process
        """
        lines = os.popen("ps aux").read().splitlines()
        ob = os.popen("which openbox").read().strip()
        for line in lines:
            if ob in " ".join(line.split()[10:]):
                os.kill(int(line.split()[1]), 12)
                break


    def setChanged(self, status=True):
        """
        Sets the changed flag and updates window title
        """
        title = str(self.parent().windowTitle())
        
        if status and self.changed is False:
            self.parent().setWindowTitle(title + " *")
        elif status is False and self.changed is True:        
            newTitle = title[0:-2]
            self.parent().setWindowTitle(newTitle)
            
        self.changed = status


    def updateExecute(self, newExecute):
        """
        Updates the execute field of a menu item
        """
        nodeIndex = self.treeMenu.currentIndex()
        # print self.treeMenu.currentItem().parent().text(0)

        index = self.treeMenu.currentIndex().row()
        id = self.txtID.text()

        if len(id) < 1:
            id = "root-menu"

        self.obMenu.setMenuExecute(id, index, newExecute)
        self.setChanged()