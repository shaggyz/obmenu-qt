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
        self.init_tree()

        # Combo options
        actions = []
        actions.append("Execute")
        actions.append("Reconfigure")
        actions.append("Restart")
        actions.append("Exit")
        self.cmbAction.addItems(actions)
        
        # all controls disabled
        self.txtLabel.setDisabled(True)
        self.txtID.setDisabled(True)
        self.txtExecute.setDisabled(True)
        self.cmbAction.setDisabled(True)

        # tree columns
        self.treeMenu.header().setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        self.changed = False


    def init_tree(self):
        """
        Configures the tree initial state
        """
        self.treeMenu.clear()
        self.treeMenu.setColumnCount(5)
        self.treeMenu.setHeaderLabels(["Label", "Type", "Action", "Execute", "ID"])
        self.treeMenu.setSortingEnabled(False)
        self.treeMenu.setAlternatingRowColors(True)
        self.treeMenu.setColumnWidth(0, 150)

        self.file_path = self.get_base_menu_file()

        if self.file_path:

            self.ob_menu = ObMenuXml(self.file_path)
            
            if not self.ob_menu.load_xml():
                # TODO: QMessageBox here
                print "Error during xml load"
                return
            
            menu = self.ob_menu.get_menu()
            menu_id = menu.get("id")

            # tree root
            self.root_tree = QtGui.QTreeWidgetItem(self.treeMenu)
            self.root_tree.setText(0, menu.get("label"))
            self.root_tree.setText(1, self.ob_menu.get_item_tag(menu))
            self.root_tree.setText(4, menu.get("id"))

            # children items
            self.load_menu(menu)

            self.root_tree.setExpanded(True)

            # signal connections
            self.connect_signals()


    def load_menu(self, menu, parent=None):
        """
        Iterates over all the menu nodes recursively 
        and creates the items for QTreeWidget
        """
        icon_path = os.getcwd() + "/icons/"

        if parent is None:
            parent = self.root_tree

        if len(menu):
            for element in menu:
                if self.ob_menu.is_comment(element):
                    continue
                
                child = QtGui.QTreeWidgetItem(parent)
                item_type = self.ob_menu.get_item_tag(element)

                # label
                if "label" in element.keys():
                    child.setText(0, element.get("label"))

                # type
                child.setText(1, item_type)

                # id
                if "id" in element.keys():
                    child.setText(4, element.get("id"))

                if item_type == "menu":
                    # icon
                    if "icon" in element.keys():
                        child.setIcon(0, QtGui.QIcon(element.get("icon")))
                    else:
                        child.setIcon(0, QtGui.QIcon(icon_path + "document-open-folder.png"))
                    # if a menu does not have label 
                    # the id attribute is used instead
                    if "label" not in element.keys():
                        label = element.get("id")
                        child.setText(0, label)
                    if len(element):
                        self.load_menu(element, child)
                if item_type == "item":
                    #icon
                    if "icon" in element.keys():
                        child.setIcon(0, QtGui.QIcon(element.get("icon")))
                    else: 
                        child.setIcon(0, QtGui.QIcon(icon_path + "application-x-desktop.png"))
                    # we need to find actions
                    if len(element):
                        action = element[0]
                        child.setText(2, action.get("name"))

                        # action childs
                        if len(action):
                            for item in action:
                                # execute
                                if self.ob_menu.get_item_tag(item) == "execute":
                                    child.setText(3, item.text)
                if item_type == "separator":
                    child.setIcon(0, QtGui.QIcon(icon_path + "separator.png"))
                    child.setText(2, "---")
                    child.setText(3, "---")
                    child.setText(4, "---")

    def get_base_menu_file(self):
        """
        Gets the main openbox menu file
        """
        menu_path = os.getenv("HOME") + "/.config/openbox/menu.xml"
        # menu_path = os.getenv("HOME") + "/menu.xml"

        if not os.path.isfile(menu_path):
            QtGui.QMessageBox.warning(self, 
                "Missing menu file", 
                "You dont seems to have a openbox menu file in the default location: %s" % (menu_path))
            return None

        return menu_path


    def connect_signals(self):
        """
        Connects internal widget signals
        """
        self.treeMenu.itemPressed.connect(self.load_item)
        self.txtLabel.textEdited.connect(self.update_selected_item)
        self.txtID.textEdited.connect(self.update_selected_item)
        self.cmbAction.activated.connect(self.update_selected_item)
        self.txtExecute.textEdited.connect(self.update_selected_item)


    def load_item(self, item, column=0):
        """
        Item pressed slot (loads an item on controls for edition)
        """
        self.txtLabel.setText(item.text(0))
        item_type = item.text(1)
        selIndex = self.cmbAction.findText(item.text(2))
        self.txtExecute.setText(item.text(3))
        self.txtID.setText(item.text(4))
        
        self.cmbAction.setDisabled(selIndex == -1)
        self.cmbAction.setCurrentIndex(selIndex)

        self.parent().menuActionMoveUp.setDisabled(True)            
        self.parent().menuActionMoveDown.setDisabled(True)            

        # widget status in function of 
        # selected item type
        if item_type == "separator":

            self.txtLabel.setDisabled(True)
            self.txtID.setDisabled(True)
            self.txtExecute.setDisabled(True)
            self.cmbAction.setDisabled(True)

        elif item_type == "menu":

            self.txtLabel.setDisabled(False)
            self.txtID.setDisabled(False)
            self.txtExecute.setDisabled(True)
            self.cmbAction.setDisabled(True)

        elif item_type == "item":

            self.txtLabel.setDisabled(False)
            self.txtID.setDisabled(False)
            self.txtExecute.setDisabled(False)
            self.cmbAction.setDisabled(False)

        self.parent().menuActionDelete.setDisabled(False)

        # Move buttons
        current_index = self.treeMenu.currentIndex().row()

        if current_index > 0:
            self.parent().menuActionMoveUp.setDisabled(False)            

        if item.parent() and current_index < (item.parent().childCount()-1):
            self.parent().menuActionMoveDown.setDisabled(False)            


    def reconfigure_openbox(self):
        """
        Kills the openbox process
        """
        lines = os.popen("ps aux").read().splitlines()
        ob = os.popen("which openbox").read().strip()
        for line in lines:
            if ob in " ".join(line.split()[10:]):
                os.kill(int(line.split()[1]), 12)
                break


    def set_changed(self, status=True):
        """
        Sets the changed flag and updates window title
        """
        title = str(self.parent().windowTitle())
        
        if status and self.changed is False:
            self.parent().menuActionSave.setDisabled(False)
            self.parent().setWindowTitle(title + " *")
        elif status is False and self.changed is True:        
            newTitle = title[0:-2]
            self.parent().setWindowTitle(newTitle)
            self.parent().menuActionSave.setDisabled(True)
            
        self.changed = status

    def _get_parent_id(self, item):
        """
        Returns the parent item id
        """
        parent = item.parent()
        if parent:
            parent_id = parent.text(4)
        else:
            parent_id = "root-menu"
        return parent_id

    def update_selected_item(self):
        """
        Updates all the item fields on dom object
        """
        current_item = self.treeMenu.currentItem()

        if current_item:

            parent_id = self._get_parent_id(current_item)
            index = self.treeMenu.currentIndex().row()

            (id, label, action, execute_, item_type) = self.read_item_fields()

            if id and len(id):
                id = unicode(id)

            if item_type == "item":
                self.ob_menu.edit_item("item", parent_id, index, unicode(label), unicode(action), unicode(execute_), icon=None, new_id=id)
            elif item_type == "menu":
                self.ob_menu.edit_item("menu", parent_id, index, label=unicode(label), new_id=id)
            
            current_item.setText(0, label)
            current_item.setText(2, action)
            current_item.setText(3, execute_)

            if id:
                current_item.setText(4, id)

            self.set_changed()

    def read_item_fields(self):
        """
        Returns a tuple with the item fields from edit widgets
        """
        current_item = self.treeMenu.currentItem()

        id = None if len(self.txtID.text()) < 1 else self.txtID.text()

        label = self.txtLabel.text()
        action = self.cmbAction.currentText()
        exe = self.txtExecute.text()
        item_type = current_item.text(1)

        return (id, label, action, exe, item_type)

    def new_item(self):
        """
        Adds a new item to dom object
        """
        current_item = self.treeMenu.currentItem()
        parent_id = self._get_parent_id(current_item)
        index = self.treeMenu.currentIndex().row() + 1
        parent = current_item.parent()

        label = "New item"
        action = "Execute"
        execute_ = "command"

        self.ob_menu.add_item(label, action, execute_, parent_id, index)

        # new node for tree-view
        child = QtGui.QTreeWidgetItem()
        child.setText(0, label)
        child.setText(1, "item")
        child.setText(2, action)
        child.setText(3, execute_)
        parent.insertChild(index, child)

        # ui update
        self.treeMenu.scrollToItem(child)
        self.treeMenu.setCurrentItem(child)
        child.setSelected(True)
        self.load_item(child)
        self.set_changed()

    def new_separator(self):
        """
        Adds a new item separator 
        """
        current_item = self.treeMenu.currentItem()
        parent_id = self._get_parent_id(current_item)
        index = self.treeMenu.currentIndex().row() + 1
        parent = current_item.parent()

        # Menu bounds: no items 
        # allowed over root-menu level
        if parent is None:
            parent = current_item

        self.ob_menu.add_separator(parent_id, index)

        # new node for tree-view
        child = QtGui.QTreeWidgetItem()
        child.setText(1, "separator")
        parent.insertChild(index, child)

        current_item.setSelected(False)
        child.setSelected(True)
        self.set_changed()

    def new_submenu(self):
        """
        Adds a new submenu
        """
        current_item = self.treeMenu.currentItem()
        parent_id = self._get_parent_id(current_item)
        index = self.treeMenu.currentIndex().row() + 1
        parent = current_item.parent()

        id = "new-submenu"
        label = "New Submenu"

        default_node = self.ob_menu.add_submenu(id, label, parent_id, index)

        # new node for tree-view
        child = QtGui.QTreeWidgetItem()
        child.setText(0, label)
        child.setText(1, "menu")
        child.setText(4, id)

        default_item = QtGui.QTreeWidgetItem()
        default_item.setText(0, "New item")
        default_item.setText(1, "item")
        default_item.setText(2, "Execute")
        default_item.setText(3, "command")

        child.insertChild(0, default_item)
        parent.insertChild(index, child)

        self.treeMenu.setCurrentItem(default_item)
        self.load_item(default_item)
        self.set_changed()

    def remove_item(self):
        """
        Remove current item (only on dom memory)
        """
        current_item = self.treeMenu.currentItem()
        item_type = current_item.text(1)
        index = self.treeMenu.currentIndex().row()
        parent_id = self._get_parent_id(current_item)        

        if self.ob_menu.remove_item(item_type, index, parent_id):
            self.parent().statusBar().showMessage("Item removed", 3000)
        else:
            self.parent().statusBar().showMessage("Error during item elimination", 3000)

        parent = current_item.parent()
        parent.removeChild(current_item)

        self.set_changed()

    def move_item_up(self):
        """
        Slot: moves current item up
        """
        self._move_item("up")

    def move_item_down(self):
        """
        Slot: moves current item down
        """
        self._move_item("down")

    def _move_item(self, direction):
        """
        Moves an item position up or down
        """
        item = self.treeMenu.currentItem()
        index = self.treeMenu.currentIndex().row()
        item_type = item.text(1)
        parent_id = self._get_parent_id(item)        

        parent = item.parent()
        clone = parent.takeChild(index)

        if direction == "up":
            if index > 0:
                new_index = index - 1  
            else:
                self.parent().statusBar().showMessage("Item top limit", 3000)
                return
        else:
            new_index = index + 1
            if new_index >= parent.childCount():
                self.parent().statusBar().showMessage("Item bottom limit", 3000)
                return

        parent.setExpanded(True)
        clone.setExpanded(True)

        parent.insertChild(new_index, clone)
        self.ob_menu.move_item(item_type, index, new_index, parent_id, parent_id)
        self.treeMenu.setCurrentItem(clone)
        self.load_item(clone)

        self.set_changed()


    def save_changes(self):
        """
        Slot: Saves changes (stored on dom object)
        """
        if self.changed:
            if self.ob_menu.save_menu():
                self.reconfigure_openbox()
                self.set_changed(False)
                self.parent().statusBar().showMessage("Changes saved", 3000)
                self.init_tree()
            else:
                self.parent().statusBar().showMessage("Error saving changes", 3000)    
        else: 
            self.parent().statusBar().showMessage("No chanches detected", 3000)

