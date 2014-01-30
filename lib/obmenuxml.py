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
            root = self.tree.getroot()

            if len(root) < 1:
                raise Exception("Invalid menu")
            
            self.menu = root[0]
            self.debug()

            return True

        except (IOError, Exception), e:
            print e
            return False


    def get_xml(self):
        """
        Returns the complete xml on a string
        """
        return etree.tostring(self.menu, pretty_print=True)


    def debug(self):
        """
        Tests and debugs
        """
        root = self.tree.getroot()

        print "=== root ==="
        print "tag: " + root.xpath('local-name()')
        print "with %i children" % (len(root))

        print "\n=== menu ==="
        print "with %i children" % (len(self.menu))
        print "tag: " + self.menu.xpath('local-name()')
        print "id: " + self.menu.get("id")
        print "label: " + self.menu.get("label")

        print "\n"



"""
Static application entry poiny
"""
if __name__ == "__main__":
    app = ObMenuXml("/home/shaggyz/menu.xml")
    print "Resultado load_xml: %i" % (app.load_xml())




