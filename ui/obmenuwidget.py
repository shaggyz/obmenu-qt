# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from ui.obmenu import Ui_frmObmenu

class ObMenuWidget(Ui_frmObmenu, QtGui.QWidget):
    """
    QtCreator generated file overload
    """
    def __init__(self):
        """
        Constructs the main window
        """
        super(QtGui.QWidget, self).__init__()
        
        self.setupUi(self)
        self.initTree()


    def initTree(self):
        """
        Configures the tree initial state
        """
        self.treeMenu.setColumnCount(4)
        self.treeMenu.setHeaderLabels(["Label", "Type", "Action", "Execute"])
        self.treeMenu.setSortingEnabled(True)
        self.treeMenu.setAlternatingRowColors(True)

        # tree root
        rootTree = QtGui.QTreeWidgetItem(self.treeMenu)
        rootTree.setText(0, "Openbox 3")
        rootTree.setText(1, "menu")

        for x in xrange(1,10):
            child = QtGui.QTreeWidgetItem(rootTree)
            child.setText(0, "foo " + str(x))
            child.setText(1, "bar" + str(x))

        rootTree.setExpanded(True)