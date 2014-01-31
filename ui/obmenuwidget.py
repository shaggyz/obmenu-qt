# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from ui.obmenu import Ui_frmObmenu
from lib.obmenuxml import ObMenuXml
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

        self.filePath = self.getBaseMenuFile()

        if self.filePath:

            self.obMenu = ObMenuXml(self.filePath)
            
            if not self.obMenu.load_xml():
                # TODO: QMessageBox here
                print "Error during xml load"
                return
            
            menu = self.obMenu.get_menu()
            menu_id = menu.get("id")

            # tree root
            self.rootTree = QtGui.QTreeWidgetItem(self.treeMenu)
            self.rootTree.setText(0, menu.get("label"))
            self.rootTree.setText(1, self.obMenu.get_item_tag(menu))
            self.rootTree.setText(4, menu.get("id"))

            # children items
            self.loadMenu(menu)

            self.rootTree.setExpanded(True)

            # signal connections
            self.connectSignals()


    def loadMenu(self, menu, parent=None):
        """
        Iterates over all the menu nodes recursively 
        and creates the items for QTreeWidget
        """
        if parent is None:
            parent = self.rootTree

        if len(menu):
            for element in menu:
                if self.obMenu.is_comment(element):
                    continue
                
                child = QtGui.QTreeWidgetItem(parent)
                item_type = self.obMenu.get_item_tag(element)

                # label
                if "label" in element.keys():
                    child.setText(0, element.get("label"))

                # type
                child.setText(1, item_type)

                # label
                if "id" in element.keys():
                    child.setText(4, element.get("id"))

                if item_type == "menu":
                    # menu elements use id as label
                    child.setText(0, element.get("id"))
                    # TODO: iterate submenu elements
                if item_type == "item":
                    
                    # we need to find actions
                    if len(element):
                        action = element[0]
                        child.setText(2, action.get("name"))

                        # action childs
                        if len(action):
                            for item in action:
                                # execute
                                if self.obMenu.get_item_tag(item) == "execute":
                                    child.setText(3, item.text)

    def getBaseMenuFile(self):
        """
        Gets the main openbox menu file
        """
        # menu_path = os.getenv("HOME") + "/.config/openbox/menu.xml"
        menu_path = os.getenv("HOME") + "/menu.xml"

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
        self.txtLabel.textEdited.connect(self.updateSelectedItem)
        self.txtID.textEdited.connect(self.updateSelectedItem)
        self.cmbAction.currentIndexChanged.connect(self.updateSelectedItem)
        self.txtExecute.textEdited.connect(self.updateSelectedItem)


    def loadItem(self, item, column=0):
        """
        Item pressed slot (loads an item on controls for edition)
        """
        self.txtLabel.setText(item.text(0))
        self.txtID.setText(item.text(4))
        itemType = item.text(1)
        
        selIndex = self.cmbAction.findText(item.text(2))
        self.cmbAction.setDisabled(selIndex == -1)
        self.cmbAction.setCurrentIndex(selIndex)

        controlsDisabled = itemType == "separator"
        self.txtLabel.setDisabled(controlsDisabled)
        self.txtID.setDisabled(controlsDisabled)
        self.txtExecute.setDisabled(controlsDisabled)

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


    def updateSelectedItem(self):
        """
        Updates all the item fields on dom object
        """
        currentItem = self.treeMenu.currentItem()

        if currentItem:
            nodeIndex = self.treeMenu.currentIndex()
            index = self.treeMenu.currentIndex().row()

            (id, label, action, exe, itemType) = self.readItemFields()

            if itemType == "item":
                self.obMenu.setItemProps(id, index, label, action, exe)
            elif itemType == "menu":
                # TODO: obxml fails on setMenuExecute and the 
                #       original prog seems to not be capable 
                #       to edit menu type items
                #self.obMenu.setMenuExecute(id, index, exe)
                print "bypass menu-type item edition"
                return
            
            currentItem.setText(0, label)
            currentItem.setText(2, action)
            currentItem.setText(3, exe)

            self.setChanged()


    def readItemFields(self):
        """
        Returns a tuple with the item fields from edit widgets
        """
        currentItem = self.treeMenu.currentItem()

        id = "root-menu" if len(self.txtID.text()) < 1 else self.txtID.text()

        label = self.txtLabel.text()
        action = self.cmbAction.currentText()
        exe = self.txtExecute.text()
        itemType = currentItem.text(1)

        return (id, label, action, exe, itemType)


    def newItem(self):
        """
        Adds a new item to dom object
        """
        currentItem = self.treeMenu.currentItem()

        label = "New Item"
        action = "Execute"
        exe = "command"

        if len(currentItem.text(4)) < 1:
            menu = "root-menu"
            parent = self.rootTree
        else: 
            parent = currentItem
            currentItem.text(4)

        position = self.treeMenu.currentIndex().row()

        # writes changes on memory
        self.obMenu.createItem(menu, label, action, exe, position)

        # new node for tree-view
        child = QtGui.QTreeWidgetItem()
        child.setText(0, label)
        child.setText(1, "item")
        child.setText(2, action)
        child.setText(3, exe)
        parent.insertChild(position, child)

        # ui update
        self.treeMenu.scrollToItem(child)
        self.treeMenu.setCurrentItem(child)
        child.setSelected(True)
        self.loadItem(child)
        self.setChanged()


    def removeItem(self):
        """
        Remove current item (only on dom memory)
        """
        currentItem = self.treeMenu.currentItem()
        position = self.treeMenu.currentIndex().row()
        
        if len(currentItem.text(4)) < 1:
            menu = "root-menu"
            parent = self.rootTree
        else: 
            parent = currentItem
            currentItem.text(4)

        print "Item on position %s from menu-id %s will be removed" % (position, menu)
        self.obMenu.removeItem(menu, position)

        parent.removeChild(currentItem)

        self.setChanged()


    def saveChanges(self):
        """
        Slot: Saves changes (stored on dom object)
        """
        if self.changed:
            self.obMenu.saveMenu(self.filePath)
            self.reconfigureOpenbox()
            self.setChanged(False)
            self.parent().statusBar().showMessage("Changes saved", 3000)
        else: 
            self.parent().statusBar().showMessage("No chanches detected", 3000)