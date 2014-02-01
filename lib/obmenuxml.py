# -*- coding: utf-8 -*-

from lxml import etree

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
            self.debug()

            return True

        except (IOError, Exception), e:
            print e
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
            if new_id is not None:
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

    def _get_item(self, type_, index, parent_id=None):
        """
        Search and get a certain node from tree
        """
        if parent_id is None:
            parent_id = "root-menu"

        submenu = self._get_submenu(parent_id)

        for element in submenu.iter("{http://openbox.org/}" + type_):
            element_index = element.getparent().index(element)
            if element_index == index:
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

    def add_item(self, label, execute_, action="Execute", parent_id=None, index=0):
        """
        Adds a new item to menu
        """
        if parent_id is None:
            parent_id = "root-menu"

        item = self._create_item(label, execute_, action)

        parent = self._get_submenu(parent_id)
        parent.insert(index, item)


    def add_submenu(self, id, label, parent_id=None, index=0):
        """
        Adds a new menu
        """
        menu_item = etree.Element("menu")
        menu_item.set("id", id)
        menu_item.set("label", label)
        # TODO: icon here
        
        menu_item.append(self._create_item("New item", "command", "Execute"))

        if parent_id is None:
            parent_id = "root-menu"

        parent = self._get_submenu(parent_id)
        parent.insert(index, menu_item)

    def add_separator(self, parent_id=None, index=0):
        """
        Add a new separator
        """
        if parent_id is None:
            parent_id = "root-menu"

        separator = etree.Element("separator")
        parent = self._get_submenu(parent_id)

        # index must be incressed to be placed bottom
        parent.insert(index + 1, separator)


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

    def debug(self):
        """
        Tests and debugs
        """
        root = self.tree.getroot()

        # print "=== root ===\n"
        # print "tag: " + root.xpath('local-name()')
        # print "with %i children" % (len(root))

        # print "\n=== menu ===\n"
        # print "with %i children" % (len(self.menu))
        # print "tag: " + self.menu.xpath('local-name()')
        # print "id: " + self.menu.get("id")
        # print "label: " + self.menu.get("label")

        # self._get_node("item", None)
        # self._get_submenu("/Debian")
        # item = self._get_item("item", 3)
        # self.edit_item(type_="item", index=2, label="El cliente de correo", action="Terminate", execute_="format C:")
        # item = self._get_item("item", 2)

        # self.add_item(u"Camaron", "comando", index=3)
        
        # self.add_submenu("SUBMENU", "El submenu")
        # self.add_separator(index=2, parent_id="sub-menu")

        # action_item = self._get_item_element("execute", item)
        # self.save_menu()

        # print etree.tostring(item, pretty_print=True)
        # print etree.tostring(action_item, pretty_print=True)
        

        # print "\n=== items ===\n"
        # for element in self.menu:
        #     if self.is_comment(element):
        #         continue
        #     print "--- %s ---" % (self.get_item_tag(element))

        #     print "\t\t--- children: ---"
        #     for child in element:
        #         print "\t\t--- %s ---" % (self.get_item_tag(child))

        # print "\n"


"""
Static application entry poiny
"""
if __name__ == "__main__":
    app = ObMenuXml("/Users/shaggyz/menu.xml")
    app.load_xml()



