# -*- coding: utf-8 -*-

from lib.obmenuxml import ObMenuXml 
from lxml import etree
import unittest, os

class TestObMenuXml(unittest.TestCase):

    def setUp(self):
        file_path = os.getcwd() + "/tests/menu.xml"
        self.ob = ObMenuXml(file_path)
        self.ob.load_xml()

        unittest.TestCase.setUp(self)

    def test_xml_loading(self):
        self.assertTrue(self.ob.load_xml())

    def test_root_element(self):
        menu = self.ob.get_menu()
        self.assertEqual(len(menu), 19)

    def test_get_xml(self):
        code = self.ob.get_xml()
        self.assertNotEqual(len(code), 0)

    def test_get_root_submenu(self):
        submenu = self.ob._get_submenu("root-menu")
        self.assertIsInstance(submenu, etree._Element)

    def test_get_debian_submenu(self):
        submenu = self.ob._get_submenu("/Debian")
        self.assertIsInstance(submenu, etree._Element)

    def test_get_fixed_item(self):
        item = self.ob._get_item("item", 3)
        self.assertIsInstance(item, etree._Element)
        self.assertEqual(item.get("label"), "Web browser")

    def test_get_item_element(self):
        item = self.ob._get_item("item", 0)
        element = self.ob._get_item_element("action", item)
        self.assertIsInstance(item, etree._Element)
        self.assertEqual(element.get("name"), "Execute")

    def test_save_menu(self):
        self.assertTrue(self.ob.save_menu())