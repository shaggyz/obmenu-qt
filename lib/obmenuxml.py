# -*- coding: utf-8 -*-

from lxml import etree
import copy

class ObMenuXml(object):
    """
    Class implemented by openbox menu interface
    """

    def __init__(self, file_path):
        """
        Sets the xml file path
        """
        self.file_path = file_path
        self.tree = None
        self.menu = None

    def load_xml(self):
        """
        Loads xml on element tree object
        """
        try:
            parser = etree.XMLParser(remove_blank_text=True)
            self.tree = etree.parse(self.file_path, parser)

            root = self.get_root()
            self.menu = root[0]
            return True

        except (IOError, Exception), e:
            return False

    def get_tree(self):
        """
        Returns the dom tree (etree Element)
        """
        return self.tree

    def get_root(self):
        """
        Return the root xml element: <openbox_menu> 
        """
        root = self.tree.getroot()

        if len(root) < 1:
            raise Exception("Invalid menu")
        
        return root

    def get_menu(self):
        """
        Return the root menu element <menu>
        """
        return self.menu

    def get_xml(self):
        """
        Returns the complete xml on a string
        """
        return etree.tostring(self.menu, pretty_print=True)

    def get_item_tag(self, item):
        """
        Returns the element xml tag
        """
        return item.xpath('local-name()')

    def is_comment(self, node):
        """
        Rerturns a boolean that indicates if node is a xml comment
        """
        return node.tag is etree.Comment

    def edit_item(self, type_, parent_id=None, index=0, label=None, action=None, execute_=None, icon=None, new_id=None):
        """
        Edit a menu item
        """
        if "separator" == type_:
            return 

        item = self._get_item(type_, index, parent_id)

        if isinstance(item, etree._Element):
            if label is not None:
                item.set("label", label)
            if icon is not None:
                item.set("label", icon)
            if new_id is not None and len(new_id):
                item.set("id", new_id)
            if "item" == type_:
                if action is not None:
                    action_item = self._get_item_element("action", item)
                    action_item.set("name", action)
                if execute_ is not None:
                    execute_item = self._get_item_element("execute", item)
                    execute_item.text = execute_

            return True

        return False

    def _get_item(self, type_, index, parent_id="root-menu"):
        """
        Search and get a certain node from tree
        """
        submenu = self._get_submenu(parent_id)
        # item type iteration filter produces segmention fault on python 2.7.x
        for element in submenu.iter():
            element_index = element.getparent().index(element)
            if element_index == index and self.get_item_tag(element) == type_:
                return element

    def _get_submenu(self, id, parent=None):
        """
        Returns a submenu from his id
        """
        if parent is None:
            parent = self.menu

        for element in parent.iter("{http://openbox.org/}menu"):
            if element.get("id") == id:
                return element

    def _get_item_element(self, element_name, item):
        """
        Return an item element from his name
        """
        if len(item):
            for element in item.iter("*"):
                if element_name == self.get_item_tag(element):
                    return element

    def save_menu(self, file_path=None):
        """
        Saves the current xml loaded on memory to a file 
        If file file path is none the current file will be overwritten
        """
        try:
            if file_path is None:
                file_path = self.file_path

            self.tree.write(file_path, pretty_print=True)
            return True
        except Exception, e:
            print e
            return False

    def add_item(self, label, execute_, action="Execute", parent_id="root-menu", index=0):
        """
        Adds a new item to menu
        """
        item = self._create_item(label, execute_, action)

        parent = self._get_submenu(parent_id)
        parent.insert(index, item)

    def add_submenu(self, id, label, parent_id="root-menu", index=0):
        """
        Adds a new menu
        """
        menu_item = etree.Element("menu")
        menu_item.set("id", id)
        menu_item.set("label", label)
        # TODO: icon here
        
        menu_item.append(self._create_item("New item", "command", "Execute"))

        parent = self._get_submenu(parent_id)
        parent.insert(index, menu_item)

    def add_separator(self, parent_id="root-menu", index=0):
        """
        Add a new separator
        """
        separator = etree.Element("separator")
        parent = self._get_submenu(parent_id)

        parent.insert(index, separator)


    def _create_item(self, label, execute_, action):
        """
        Returns an item node with default values
        """
        item = etree.Element("item")
        item.set("label", label)
        # TODO: icon here

        action_item = etree.Element("action")
        action_item.set("name", action)

        execute_item = etree.Element("execute")
        execute_item.text = execute_
        action_item.append(execute_item)
        item.append(action_item)

        return item

    def move_item(self, type_, orig_index, dest_index, dest_parent_id="root-menu", orig_parent_id="root-menu"):
        """
        moves an item position on menu
        """
        item = self._get_item(type_, orig_index, orig_parent_id)

        dest_parent = self._get_submenu(dest_parent_id)
        orig_parent = self._get_submenu(orig_parent_id)

        clone = copy.deepcopy(item)
        orig_parent.remove(item)

        dest_parent.insert(dest_index, clone)

    def remove_item(self, type_, index, parent_id="root-menu", id_=None):
        """
        Removes an item from menu
        """
        if type_ == "menu":
            item = self._get_submenu(id_)
        else:
            item = self._get_item(type_, index, parent_id)

        parent = item.getparent()

        if isinstance(item, etree._Element):
            parent.remove(item)
            return True
        else:
            return False
