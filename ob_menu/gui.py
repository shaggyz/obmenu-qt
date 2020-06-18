
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow


class Application:
    """ Wrapper class for the main application """

    @staticmethod
    def start():
        """ Static entry point the the GUI application """
        app = QApplication(sys.argv)
        window = QMainWindow()
        window.show()
        sys.exit(app.exec_())
