
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
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
                item = QTreeWidgetItem(main)
                item.setText(0, str(entry))
            elif entry.tag == '{http://openbox.org/}item':
                item = QTreeWidgetItem(main)
                item.setText(0, entry.get("label"))
            elif entry.tag == '{http://openbox.org/}separator':
                item = QTreeWidgetItem(main)
                item.setText(0, '------------')
            elif entry.tag == '{http://openbox.org/}menu':
                item = QTreeWidgetItem(main)
                item.setText(0, entry.get("label") or entry.get('id'))
            else:
                print("Unknown tag: %s" % entry.tag)
                print(entry)

        main.setExpanded(True)


class ItemEditor(QWidget):
    """ The item editor widget """
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.addWidget(QLabel("test"))



class MainWindow(QMainWindow):

    def _configure_window(self):
        self._configure_menu()
        self.tree_view = TreeView()
        self._load_items()
        self.statusBar().showMessage('Ready')

    def _load_items(self):
        menu = OpenBoxMenu()
        items = menu.parse()

        self.tree_view.load_tems(items)
        container = QWidget()
        editor = ItemEditor()

        layout = QVBoxLayout()
        layout.addWidget(self.tree_view)
        layout.addWidget(editor)

        container.setLayout(layout)

        self.setCentralWidget(container)

    def _configure_menu(self):
        menu_bar = self.menuBar()

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
