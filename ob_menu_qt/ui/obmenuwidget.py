# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import new
from ob_menu_qt.ui.obmenu import Ui_frmObmenu
from ob_menu_qt.lib.obmenuxml import ObMenuXml
import os

class ObMenuWidget(Ui_frmObmenu, QtGui.QWidget):
    """
    Main widget container designed to deal with
    the obmenuxml module, QtCreator generated
    file overload
    """
    COL_LABEL = 0
    COL_TYPE = 1
    COL_ACTION = 2
    COL_EXECUTE = 3
    COL_ID = 4
    COL_ICON = 5
    COL_PROMPT = 6

    def __init__(self, icon_path):
        """
        Constructs the main window
        """
        super(QtGui.QWidget, self).__init__()
        self.setupUi(self)
        self.icon_path = icon_path

        # current file path
        self.file_path = self.get_base_menu_file()

        # selected item reminder
        self.last_selected = None
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
        self.txtIcon.setDisabled(True)
        self.btnChangeIcon.setDisabled(True)
        self.btnPrompt.setDisabled(True)
        self.btnPrompt.setIcon(QtGui.QIcon(icon_path + "view-conversation-balloon.png"))

        # tree columns
        self.treeMenu.header().setResizeMode(self.COL_LABEL, QtGui.QHeaderView.ResizeToContents)
        self.changed = False

        # signal connections
        self.connect_signals()

    def init_tree(self):
        """
        Configures the tree initial state
        """
        self.treeMenu.clear()
        self.treeMenu.setColumnCount(6)
        self.treeMenu.setHeaderLabels(["Label", "Type", "Action", "Execute", "ID", "Icon", "Prompt"])
        self.treeMenu.setSortingEnabled(False)
        self.treeMenu.setAlternatingRowColors(True)
        self.treeMenu.setColumnWidth(self.COL_LABEL, 150)

        self.treeMenu.setColumnHidden(self.COL_ICON, True)
        self.treeMenu.setColumnHidden(self.COL_PROMPT, True)

        if self.file_path:

            self.ob_menu = ObMenuXml(self.file_path)
            
            if not self.ob_menu.load_xml():
                QtGui.QMessageBox.critical(self,
                                          "Error on XML load",
                                          "The application can't read the xml file, may be is corrupted")
                return
            
            menu = self.ob_menu.get_menu()

            # tree root
            self.root_tree = QtGui.QTreeWidgetItem(self.treeMenu)
            self.root_tree.setText(self.COL_LABEL, menu.get("label"))
            self.root_tree.setText(self.COL_TYPE, self.ob_menu.get_item_tag(menu))
            self.root_tree.setText(self.COL_ID, menu.get("id"))

            # children items
            self.load_menu(menu)
            self.root_tree.setExpanded(True)

    def load_menu(self, menu, parent=None):
        """
        Iterates over all the menu nodes recursively 
        and creates the items for QTreeWidget
        """
        if parent is None:
            parent = self.root_tree

        if len(menu):
            index = 0
            for element in menu:
                if self.ob_menu.is_comment(element):
                    continue

                child = QtGui.QTreeWidgetItem(parent)
                item_type = self.ob_menu.get_item_tag(element)

                # label
                if "label" in element.keys():
                    child.setText(self.COL_LABEL, element.get("label"))

                # type
                child.setText(self.COL_TYPE, item_type)

                # id
                if "id" in element.keys():
                    child.setText(self.COL_ID, element.get("id"))

                # icon path
                if "icon" in element.keys():
                    child.setText(self.COL_ICON, element.get("icon"))

                # previously selected
                if self.last_selected is not None:
                    last_index = self.last_selected["index"]
                    last_parent_id = self.last_selected["parent_id"]

                    if last_index == index and last_parent_id == parent.text(self.COL_ID):
                        child.setSelected(True)
                        self.treeMenu.setCurrentItem(child, 0)

                if item_type == "menu":
                    # icon
                    if "icon" in element.keys():
                        child.setIcon(self.COL_LABEL, QtGui.QIcon(element.get("icon")))
                    else:
                        child.setIcon(self.COL_LABEL, QtGui.QIcon(self.icon_path + "document-open-folder.png"))
                    # if a menu does not have label
                    # the id attribute is used instead
                    if "label" not in element.keys():
                        label = element.get("id")
                        child.setText(self.COL_LABEL, label)
                    if len(element):
                        self.load_menu(element, child)
                if item_type == "item":
                    #icon
                    if "icon" in element.keys():
                        child.setIcon(self.COL_LABEL, QtGui.QIcon(element.get("icon")))
                    else:
                        child.setIcon(self.COL_LABEL, QtGui.QIcon(self.icon_path + "application-x-desktop.png"))
                    # we need to find actions
                    if len(element):
                        action = element[0]
                        child.setText(self.COL_ACTION, action.get("name"))

                        # action childs
                        if len(action):
                            for item in action:
                                # execute
                                if self.ob_menu.get_item_tag(item) == "execute":
                                    child.setText(self.COL_EXECUTE, item.text)
                                # prompt
                                if self.ob_menu.get_item_tag(item) == "prompt":
                                    child.setText(self.COL_PROMPT, item.text)

                if item_type == "separator":
                    child.setIcon(self.COL_LABEL, QtGui.QIcon(self.icon_path + "separator.png"))
                    child.setText(self.COL_LABEL, "---")
                    child.setText(self.COL_ACTION, "---")
                    child.setText(self.COL_EXECUTE, "---")
                    child.setText(self.COL_ID, "---")

                index += 1

    def open_menu_file(self):
        """
        Slot: Opens an external menu file
        """
        file_path = QtGui.QFileDialog.getOpenFileName(self,
                                                      "Select a configuration file to load",
                                                      QtCore.QDir.home().path(),
                                                      "Configuration files (*.xml);;All files (*.*)")

        if len(file_path):

            # file changed
            if self.changed:
                user_response = QtGui.QMessageBox.question(self,
                                           "Save the changes before open",
                                           "There are unsaved changes in current file",
                                            QtGui.QMessageBox.Discard,
                                            QtGui.QMessageBox.Save,
                                            QtGui.QMessageBox.Cancel)

                # unsaved changes
                if user_response == QtGui.QMessageBox.Save:
                    self.save_changes()

            # new file
            self.file_path = str(file_path)
            self.init_tree()


    def get_base_menu_file(self):
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

    def connect_signals(self):
        """
        Connects internal widget signals
        """
        self.treeMenu.itemPressed.connect(self.load_item)
        self.txtLabel.textEdited.connect(self.update_selected_item)
        self.txtID.textEdited.connect(self.update_selected_item)
        self.cmbAction.activated.connect(self.update_selected_item)
        self.txtExecute.textEdited.connect(self.update_selected_item)
        self.txtIcon.textEdited.connect(self.update_selected_item)
        self.btnChangeIcon.clicked.connect(self.change_icon_path)
        self.btnPrompt.clicked.connect(self.update_item_prompt)

    def load_item(self, item):
        """
        Item pressed slot (loads an item on controls for edition)
        """
        self.txtLabel.setText(item.text(self.COL_LABEL))
        item_type = item.text(self.COL_TYPE)
        selIndex = self.cmbAction.findText(item.text(self.COL_ACTION))
        self.txtExecute.setText(item.text(self.COL_EXECUTE))
        self.txtID.setText(item.text(self.COL_ID))
        self.txtIcon.setText(item.text(self.COL_ICON))

        # Last selected reminder
        self._update_last_selected()
        
        self.cmbAction.setDisabled(selIndex == -1)
        self.cmbAction.setCurrentIndex(selIndex)

        # widget status in function of
        # selected item type
        if item_type == "separator":

            self.txtLabel.setDisabled(True)
            self.txtID.setDisabled(True)
            self.txtExecute.setDisabled(True)
            self.cmbAction.setDisabled(True)
            self.txtIcon.setDisabled(True)
            self.btnChangeIcon.setDisabled(True)
            self.btnPrompt.setDisabled(True)

        elif item_type == "menu":

            self.txtLabel.setDisabled(False)
            self.txtID.setDisabled(False)
            self.txtExecute.setDisabled(True)
            self.cmbAction.setDisabled(True)
            self.txtIcon.setDisabled(False)
            self.btnChangeIcon.setDisabled(False)
            self.btnPrompt.setDisabled(True)

        elif item_type == "item":

            self.txtLabel.setDisabled(False)
            self.txtID.setDisabled(False)
            self.txtExecute.setDisabled(False)
            self.cmbAction.setDisabled(False)
            self.txtIcon.setDisabled(False)
            self.btnChangeIcon.setDisabled(False)
            self.btnPrompt.setDisabled(False)

        self.parent().menuActionDelete.setDisabled(False)
        self.parent().menuActionMenu.setDisabled(False)
        self.parent().menuActionItem.setDisabled(False)
        self.parent().menuActionSeparator.setDisabled(False)

        # Move buttons
        current_index = self.treeMenu.currentIndex().row()

        # Move up/down bounds
        if current_index > 0 or item.parent().text(self.COL_ID) != "root-menu":
            self.parent().menuActionMoveUp.setDisabled(False)
        else:
            self.parent().menuActionMoveUp.setDisabled(True)

        down_bounds = item.parent() and current_index < (item.parent().childCount()-1)

        if down_bounds or item.parent().text(self.COL_ID) != "root-menu":
            self.parent().menuActionMoveDown.setDisabled(False)
        else:
            self.parent().menuActionMoveDown.setDisabled(True)

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
            self.parent().setWindowTitle(title + " - Unsaved changes")
        elif status is False and self.changed is True:        
            newTitle = title[0:-18]
            self.parent().setWindowTitle(newTitle)
            self.parent().menuActionSave.setDisabled(True)
            
        self.changed = status

    def _get_parent_id(self, item):
        """
        Returns the parent item id
        """
        parent = item.parent()
        if parent:
            parent_id = parent.text(self.COL_ID)
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

            (id, label, action, execute_, item_type, icon, prompt) = self.read_item_fields()

            if id and len(id):
                id = unicode(id)

            if prompt and len(prompt):
                prompt = unicode(prompt)

            if item_type == "item":
                self.ob_menu.edit_item("item", parent_id, index, unicode(label), unicode(action), unicode(execute_),
                                       unicode(icon), new_id=id, prompt=prompt)

            elif item_type == "menu":
                self.ob_menu.edit_item("menu", parent_id, index, label=unicode(label), new_id=id, icon=unicode(icon))
            
            current_item.setText(self.COL_LABEL, label)
            current_item.setText(self.COL_ACTION, action)
            current_item.setText(self.COL_EXECUTE, execute_)

            if prompt:
                current_item.setText(self.COL_PROMPT, prompt)

            if id:
                current_item.setText(self.COL_ID, id)

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
        item_type = current_item.text(self.COL_TYPE)
        icon = self.txtIcon.text()
        prompt = None if len(current_item.text(self.COL_PROMPT)) < 1 else current_item.text(self.COL_PROMPT)

        return (id, label, action, exe, item_type, icon, prompt)

    def new_item(self):
        """
        Adds a new item to dom object
        """
        current_item = self.treeMenu.currentItem()
        parent = current_item.parent()

        if parent is None:
            # Menu bounds: no items
            # allowed over root-menu level
            parent = current_item
            parent_id = "root-menu"
            index = 0
        elif current_item.text(self.COL_TYPE) == "menu":
            # Item on submenu
            index = 0
            parent = current_item
            parent_id = current_item.text(self.COL_ID)
        else:
            # Normal item insertion
            index = self.treeMenu.currentIndex().row() + 1
            parent_id = self._get_parent_id(current_item)

        label = "New item"
        action = "Execute"
        execute_ = "command"

        self.ob_menu.add_item(label, action, execute_, parent_id, index)

        # new node for tree-view
        child = QtGui.QTreeWidgetItem()
        child.setText(self.COL_LABEL, label)
        child.setText(self.COL_TYPE, "item")
        child.setText(self.COL_ACTION, action)
        child.setText(self.COL_EXECUTE, execute_)
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
        parent = current_item.parent()

        # Menu bounds: no items 
        # allowed over root-menu level
        if parent is None:
            parent = current_item
            parent_id = "root-menu"
            index = 0
        else:
            index = self.treeMenu.currentIndex().row() + 1
            parent_id = self._get_parent_id(current_item)

        self.ob_menu.add_separator(parent_id, index)

        # new node for tree-view
        child = QtGui.QTreeWidgetItem()
        child.setText(self.COL_TYPE, "separator")
        parent.insertChild(index, child)

        current_item.setSelected(False)
        child.setSelected(True)
        self.set_changed()

    def new_submenu(self):
        """
        Adds a new submenu
        """
        current_item = self.treeMenu.currentItem()
        parent = current_item.parent()

        # Menu bounds: no items 
        # allowed over root-menu level
        if parent is None:
            parent = current_item
            parent_id = "root-menu"
            index = 0
        else:
            index = self.treeMenu.currentIndex().row() + 1
            parent_id = self._get_parent_id(current_item)

        id = "new-submenu"
        label = "New Submenu"

        self.ob_menu.add_submenu(id, label, parent_id, index)

        # new node for tree-view
        child = QtGui.QTreeWidgetItem()
        child.setText(self.COL_LABEL, label)
        child.setText(self.COL_TYPE, "menu")
        child.setText(self.COL_ID, id)

        default_item = QtGui.QTreeWidgetItem()
        default_item.setText(self.COL_LABEL, "New item")
        default_item.setText(self.COL_TYPE, "item")
        default_item.setText(self.COL_ACTION, "Execute")
        default_item.setText(self.COL_EXECUTE, "command")

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
        item_type = current_item.text(self.COL_TYPE)
        item_id = current_item.text(self.COL_ID)
        index = self.treeMenu.currentIndex().row()
        parent_id = self._get_parent_id(current_item)

        if self.ob_menu.remove_item(item_type, index, parent_id, item_id):
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
        item_type = item.text(self.COL_TYPE)
        parent_id = self._get_parent_id(item)
        dest_parent_id = parent_id

        item_above = self.treeMenu.itemAbove(item)
        item_below = self.treeMenu.itemBelow(item)

        parent = item.parent()
        clone = parent.takeChild(index)

        if direction == "up":
            # the item is moving to another submenu
            if item_above.text(self.COL_TYPE) == "menu" or item_above.parent().text(self.COL_ID) != parent.text(self.COL_ID):
                # already child of current submenu
                if item_above.parent().text(self.COL_ID) != parent.text(self.COL_ID):
                    parent = item_above.parent()
                    new_index = parent.indexOfChild(item_above)
                    dest_parent_id = parent.text(self.COL_ID)
                else:
                    parent = item_above
                    new_index = item_above.childCount()
                    dest_parent_id = item_above.text(self.COL_ID)
            # normal movement
            elif index > 0:
                new_index = index - 1
            # menu bounds
            else:
                self.parent().statusBar().showMessage("Item top limit", 3000)
                return
        else:
            # the item is moving to another submenu
            if item_below.text(self.COL_TYPE) == "menu":
                parent = item_below
                new_index = 0
                dest_parent_id = item_below.text(self.COL_ID)
            else:
                new_index = index + 1
                # menu bounds
                if new_index > parent.childCount():
                    # already child of current submenu
                    if item_below.parent().text(self.COL_ID != parent.text(self.COL_ID)):
                        parent = item_below.parent()
                        new_index = parent.indexOfChild(item_below)
                        dest_parent_id = parent.text(self.COL_ID)
                    else:
                        self.parent().statusBar().showMessage("Item bottom limit", 3000)
                        return

        parent.setExpanded(True)
        clone.setExpanded(True)

        parent.insertChild(new_index, clone)
        self.ob_menu.move_item(item_type, index, new_index, dest_parent_id, parent_id)
        self.treeMenu.setCurrentItem(clone)
        self.load_item(clone)

        self.set_changed()

    def update_item_prompt(self):
        """
        Slot: Updates prompt property of current item
        """
        current_prompt = self.treeMenu.currentItem().text(self.COL_PROMPT).trimmed()
        new_prompt = QtGui.QInputDialog.getText(self, "Edit prompt message", "Prompt message: ", text=current_prompt)

        # accepted and changed
        if new_prompt[1] and new_prompt[0] != current_prompt:
            self.treeMenu.currentItem().setText(self.COL_PROMPT, new_prompt[0].trimmed())
            self.update_selected_item()
            self.set_changed()

    def _update_last_selected(self):
        """
        Updates the last selected reminder
        """
        item = self.treeMenu.currentItem()
        parent = item.parent()

        # root node
        if parent is None:
            return

        parent_id = parent.text(self.COL_ID)
        index = self.treeMenu.currentIndex().row()

        self.last_selected = {"index": index, "parent_id": parent_id}

    def change_icon_path(self):
        """
        Slot: called when change
        icon button is clicked
        """
        new_icon_path = QtGui.QFileDialog.getOpenFileName(self, "Select the new icon file", "/usr/share/icons", "Images (*.png *.xpm *.jpg)")
        self.txtIcon.setText(new_icon_path)
        self.update_selected_item()
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

