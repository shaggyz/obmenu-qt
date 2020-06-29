import unittest
import os
from contextlib import suppress
from ob_menu.menu import OpenBoxMenu

# Some path globals
tests_path = os.path.dirname(os.path.realpath(__file__))
debian_stub = "%s/stubs/debian.xml" % tests_path
temp_file = "%s/temp.xml" % tests_path


class TestOpenBoxMenu(unittest.TestCase):

    def test_file_load(self):
        """ Test file operations """
        menu = OpenBoxMenu(debian_stub)
        self.assertTrue(menu.is_valid(), 'A valid file is loaded')
        self.assertNotEmpty(menu.get_content(), 'The file is parsed as a non-empty dict.')
        invalid_menu = OpenBoxMenu('invalid')
        self.assertFalse(invalid_menu.is_valid(), 'An invalid file is not loaded')
        self.assertEmpty(invalid_menu.to_dict(), 'The file is parsed as an empty dict.')

    def test_parser(self):
        """ Test the menu parser """
        openbox_menu = OpenBoxMenu(debian_stub)
        content = openbox_menu.to_dict()
        # main
        main = content[0]
        self.assertEqual(main['type'], 'openbox_menu', 'The openbox_menu type is parsed')
        # root menu
        root = content['children'][0]
        self.assertEqual(root['type'], 'menu', 'The menu type is parsed')
        self.assertEqual(root['id'], 'root-menu', 'The root ID is parsed')
        self.assertEqual(root['label'], 'Openbox 3', 'The root label is parsed')
        # normal item
        item = root['children'][1]
        self.assertEqual(item['type'], 'item', 'The item type is parsed')
        self.assertIsNone(item['id'], 'Item does not contains the ID')
        self.assertEqual(item['label'], 'Web browser', 'The item label is parsed')
        exe_action = item['actions'][0]
        self.assertEqual(exe_action['name'], 'Execute', 'The execute action is parsed')
        self.assertEqual(exe_action['execute'], 'x-www-browser', 'The execute parameter is parsed')
        # sub menu
        menu = root['children'][3]
        self.assertEqual(menu['type'], 'menu', 'The sub menu type is parsed')
        self.assertEqual(menu['id'], '/Debian', 'The menu ID is parsed')
        self.assertIsNone(menu['label'], 'The menu label is None when missing')
        self.assertIsNone(menu['execute'], 'The menu execute is None when missing')
        menu = root['children'][5]
        self.assertEqual(menu['type'], 'menu', 'The sub menu type is parsed')
        self.assertEqual(menu['id'], 'applications-menu', 'The menu ID is parsed')
        self.assertEqual(menu['label'], 'Applications', 'The menu label is parsed')
        self.assertEqual(menu['execute'], '/usr/bin/obamenu', 'The menu execute is parsed')
        # separator
        separator = root['children'][4]
        self.assertEqual(separator['type'], 'separator', 'The separator type is parsed')
        self.assertIsNone(separator['id'], 'Separator without ID')
        self.assertIsNone(separator['label'], 'Separator without label')
        self.assertNotIn('execute', separator.keys(), 'A separator has no execute')
        # comment
        comment = root['children'][2]
        self.assertIsNone(comment['id'], 'Comment without ID')
        self.assertIsNone(comment['label'], 'Comment without label')
        self.assertEqual('This is a comment', comment['text'], 'The comment text is parsed')
        # special action item
        special_action = root['children'][11]
        self.assertEqual(special_action['label'], 'Exit', 'The special action label is parsed')
        self.assertEqual(special_action['type'], 'item', 'The special action item type is parsed')
        self.assertIsNone(special_action['id'], 'The special action has no ID')

    def test_file_save(self):
        """ Test file write operations """
        openbox_menu = OpenBoxMenu(debian_stub)
        with suppress(OSError): os.unlink(temp_file)
        # file creation
        openbox_menu.save(temp_file)
        self.assertTrue(os.path.isfile(temp_file), 'A file was saved at %' % temp_file)
        # XML consistency
        debian_xml = generated_file = None
        with open(debian_stub, 'r') as debian_file:
            debian_xml = debian_file.read()
        with open(temp_file, 'r') as generated_file:
            generated_xml = generated_file.read()
        self.assertIsNotNone(debian_xml, 'The debian XML is read')
        self.assertIsNotNone(generated_file, 'The generated XML is read')
        debian_xml_sanitized = debian_xml.replace('\n', '')
        generated_xml_sanitized = generated_xml.replace('\n', '')
        self.assertEqual(debian_xml_sanitized, generated_xml_sanitized, 'The XML saved to disk is unaltered')
        with suppress(OSError): os.unlink(temp_file)

    def test_move_items(self):
        """ Test move items up-down """
        openbox_menu = OpenBoxMenu(debian_stub)
        # swap terminal item by browser item
        self.assertTrue(openbox_menu.move_item_up(1))
        contents = openbox_menu.to_dict()
        item_0 = contents['children'][0]['children'][0]
        item_1 = contents['children'][0]['children'][1]
        contents = openbox_menu.to_dict()
        moved_item_0 = contents['children'][0]['children'][0]
        moved_item_1 = contents['children'][0]['children'][1]
        self.assertEqual(moved_item_0, item_1, 'Item is moved up')
        self.assertEqual(moved_item_1, item_0, 'The other item is moved down')
        # back the items to the original position
        self.assertTrue(openbox_menu.move_item_down(0))
        contents = openbox_menu.to_dict()
        moved_item_0 = contents['children'][0]['children'][0]
        moved_item_1 = contents['children'][0]['children'][1]
        self.assertEqual(moved_item_0, item_0, 'Item is moved down')
        self.assertEqual(moved_item_1, item_1, 'The other item is moved up')
        # limits
        self.assertFalse(openbox_menu.move_item_up(0), 'The first item cannot be moved up')
        self.assertFalse(openbox_menu.move_item_down(11), 'The last item cannot be moved down')

    def test_delete_item(self):
        """ Test item removal """
        openbox_menu = OpenBoxMenu(debian_stub)
        original_menu = openbox_menu.to_dict()['children'][0]['children']
        openbox_menu.delete_item(8)
        modified_menu = openbox_menu.to_dict()['children'][0]['children']
        self.assertEqual(len(original_menu) - 1, len(modified_menu), 'One item was removed')
        self.assertNotEqual(original_menu[8]['label'], modified_menu[8]['label'], 'A new item is in its place')

    def test_add_item(self):
        """ Test add a new item element """
        openbox_menu = OpenBoxMenu(debian_stub)
        original_menu = openbox_menu.to_dict()['children'][0]['children']
        self.assertTrue(openbox_menu.add_item('root-menu', label='Example', execute='example.sh'))
        modified_menu = openbox_menu.to_dict()['children'][0]['children']
        self.assertEqual(len(original_menu) + 1, len(modified_menu), 'A new item was added')
        new_item = modified_menu[len(original_menu)]
        self.assertEqual('Example', new_item['label'], 'The new item label was stored')
        self.assertEqual('example.sh', new_item['actions'][0]['execute'], 'The new item executable was stored')
        self.assertEqual('Execute', new_item['actions'][0]['name'], 'The new item execute action was stored')
        self.assertEqual('item', new_item['type'], 'The new item type is "item"')

    def test_add_separator(self):
        """ Test add a new separator element """
        openbox_menu = OpenBoxMenu(debian_stub)
        original_menu = openbox_menu.to_dict()['children'][0]['children']
        self.assertTrue(openbox_menu.add_separator('root-menu', 1), 'A separator is added')
        modified_menu = openbox_menu.to_dict()['children'][0]['children']
        self.assertEqual(len(original_menu) + 1, len(modified_menu), 'A new separator was added')
        self.assertEqual(modified_menu[2]['type'], 'separator', 'The new item is a separator')

    def test_add_menu(self):
        """ Test add a new separator element """
        openbox_menu = OpenBoxMenu(debian_stub)
        original_menu = openbox_menu.to_dict()['children'][0]['children']
        self.assertTrue(openbox_menu.add_menu('root-menu', id='example-menu', label='Example menu'), 'A new menu is added')
        modified_menu = openbox_menu.to_dict()['children'][0]['children']
        self.assertEqual(len(original_menu) + 1, len(modified_menu), 'A new menu was added')
        self.assertEqual(modified_menu[12]['type'], 'menu', 'The new item is a menu')

    @classmethod
    def tearDownClass(cls):
        """ Removes the temp. file """
        with suppress(OSError): os.unlink(temp_file)
