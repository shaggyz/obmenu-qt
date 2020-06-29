from lxml import objectify
from lxml import etree

import os
import shutil

# Openbox distribution menu config file
OB_ORIGINAL_FILE = "/etc/xdg/openbox/menu.xml"

class OpenBoxMenu:
    """ Representation of the openbox menu file """

    def __init__(self, file_path):
        """ Sets the file name """
        self.file_path = "/home/shaggyz/.config/openbox/menu.xml"
        self.menu_data = None

    def parse(self):
        """ Parse a menu file """
        contents = self._read_config_file()
        parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
        menu_data = objectify.fromstring(contents.encode('ascii'), parser=parser)
        return menu_data

    def dump(self):
        """ Converts the current menu to XML """
        print(etree.tostring(self.menu_data, pretty_print=True))

    def _read_config_file(self):
        if os.path.isfile(self.file_path):
            with open(self.file_path, 'r') as f:
                return f.read()

    def _backup(self):
        """ Creates a configuration backup """
        shutil.copyfile(self.file_path, self.file_path + ".bkp")

    @staticmethod
    def is_comment(node):
        """ returns true if the given node is an XML comment """
        return node.tag is etree.Comment

