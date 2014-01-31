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
            self.tree = etree.parse(self.file_path)
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

    def debug(self):
        """
        Tests and debugs
        """
        root = self.tree.getroot()

        print "=== root ===\n"
        print "tag: " + root.xpath('local-name()')
        print "with %i children" % (len(root))

        print "\n=== menu ===\n"
        print "with %i children" % (len(self.menu))
        print "tag: " + self.menu.xpath('local-name()')
        print "id: " + self.menu.get("id")
        print "label: " + self.menu.get("label")

        print "\n=== items ===\n"
        for element in self.menu:
            if self.is_comment(element):
                continue
            print "--- %s ---" % (self.get_item_tag(element))

            print "\t\t--- children: ---"
            for child in element:
                print "\t\t--- %s ---" % (self.get_item_tag(child))

        print "\n"



"""
Static application entry poiny
"""
if __name__ == "__main__":
    app = ObMenuXml("/home/shaggyz/menu.xml")
    print "Resultado load_xml: %i" % (app.load_xml())




