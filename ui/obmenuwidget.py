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
        self.cmbAction.setDisabled(True)

        self.changed = False


    def init_tree(self):
        """
        Configures the tree initial state
        """
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
                    # if a menu does not have label 
                    # the id attribute is used instead
                    if "label" not in element.keys():
                        label = element.get("id")
                        child.setText(0, label)
                    if len(element):
                        self.load_menu(element, child)
                if item_type == "item":
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

    def get_base_menu_file(self):
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
        self.txtID.setText(item.text(4))
        item_type = item.text(1)
        
        selIndex = self.cmbAction.findText(item.text(2))
        self.cmbAction.setDisabled(selIndex == -1)
        self.cmbAction.setCurrentIndex(selIndex)

        controls_disabled = item_type == "separator"
        self.txtLabel.setDisabled(controls_disabled)
        self.txtID.setDisabled(controls_disabled)
        self.txtExecute.setDisabled(controls_disabled)

        self.txtExecute.setText(item.text(3))


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
            self.parent().setWindowTitle(title + " *")
        elif status is False and self.changed is True:        
            newTitle = title[0:-2]
            self.parent().setWindowTitle(newTitle)
            
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
        action = "command"
        execute_ = "Execute"

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


    def remove_item(self):
        """
        Remove current item (only on dom memory)
        """
        current_item = self.treeMenu.currentItem()
        item_type = current_item.text(1)
        index = self.treeMenu.currentIndex().row()
        parent_id = self._get_parent_id(current_item)        

        self.ob_menu.remove_item(item_type, index, parent_id)

        if self.ob_menu.remove_item(item_type, index, parent_id):
            self.parent().statusBar().showMessage("Item removed", 3000)
        else:
            self.parent().statusBar().showMessage("Error during item elimination", 3000)

        parent = current_item.parent()
        parent.removeChild(current_item)

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
            else:
                self.parent().statusBar().showMessage("Error saving changes", 3000)    
        else: 
            self.parent().statusBar().showMessage("No chanches detected", 3000)

