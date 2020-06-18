
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem
from ob_menu.menu import OpenBoxMenu


class TreeView(QTreeWidget):
    """ The menu tree widget """
    COL_LABEL = 0
    COL_TYPE = 1
    COL_ACTION = 2
    COL_EXECUTE = 3
    COL_ID = 4
    COL_ICON = 5
    COL_PROMPT = 6

    def load_tems(self, items):
        """ loads the menu tree """
        root = items[0]

        self.setColumnCount(1)

        main = QTreeWidgetItem(self)
        main.setText(0, "Root")

        for entry in root:
            if OpenBoxMenu.is_comment(entry):
                continue
            if entry.tag == '{http://openbox.org/}item':
                item = QTreeWidgetItem(main)
                item.setText(0, entry.get("label"))


class MainWindow(QMainWindow):

    def _configure_window(self):
        self._configure_menu()
        self._load_items()
        self.statusBar().showMessage('Ready')

    def _load_items(self):
        menu = OpenBoxMenu()
        items = menu.parse()

        tree_view = TreeView()
        tree_view.load_tems(items)

        self.setCentralWidget(tree_view)

    def _configure_menu(self):
        menu_bar = self.menuBar()
        print("config menu")

    def show(self):
        self._configure_window()
        super().show()


class Application:
    """ Wrapper class for the main application """

    @staticmethod
    def start():
        """ Static entry point the the GUI application """
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())