# -*- coding: utf-8 -*-

from PyQt4 import QtGui

class UiMainWindow(QtGui.QMainWindow):
    
    def __init__(self):
		"""
		Constructs the main window
		"""
		super(QtGui.QMainWindow, self).__init__()

		self.setWindowTitle("Openbox menu configuration")
		self.statusBar().showMessage("Ready")
		self.initMenu()

    def initMenu(self):
        """
        Configures menu
        """	
        menu = self.menuBar()

        # --- File Menu ---

        # New
        menuActionNew = QtGui.QAction("New", self)
        menuActionNew.setShortcut("Ctrl+N")
        menuActionNew.setStatusTip("New menu file")
        
        # Open
        menuActionOpen = QtGui.QAction("Open...", self)
        menuActionOpen.setShortcut("Ctrl+O")
        menuActionOpen.setStatusTip("Open menu file...")
        
        # Save
        menuActionSave = QtGui.QAction("Save", self)
        menuActionSave.setShortcut("Ctrl+S")
        menuActionSave.setStatusTip("Save current menu")

        # Save As
        menuActionSaveAs = QtGui.QAction("Save As...", self)
        menuActionSaveAs.setShortcut("Ctrl+Shift+S")
        menuActionSaveAs.setStatusTip("Save menu as...")
        
        # Exit
        menuActionQuit = QtGui.QAction("Quit", self)
        menuActionQuit.setShortcut("Ctrl+Q")
        menuActionQuit.setStatusTip("Exits menu editor")
        
        menuFile = menu.addMenu("&File")
        menuFile.addAction(menuActionNew)
        menuFile.addAction(menuActionOpen)
        menuFile.addAction(menuActionSave)
        menuFile.addAction(menuActionSaveAs)
        menuFile.addAction(menuActionQuit)
        
        # --- Edit Menu ---

        # Move up
        menuActionMoveUp = QtGui.QAction("Move up", self)
        menuActionMoveUp.setShortcut("Ctrl+Up")
        menuActionMoveUp.setStatusTip("Move item up")

        # Move down
        menuActionMoveDown = QtGui.QAction("Move down", self)
        menuActionMoveDown.setShortcut("Ctrl+Down")
        menuActionMoveDown.setStatusTip("Move item down")

        # Delete
        menuActionDelete = QtGui.QAction("Delete", self)
        menuActionDelete.setStatusTip("Delete selected item")        
        
        menuEdit = menu.addMenu("&Edit")
        menuEdit.addAction(menuActionMoveUp)
        menuEdit.addAction(menuActionMoveDown)
        menuEdit.addAction(menuActionDelete)

        # --- Add Menu ---

        # Menu
        menuActionMenu = QtGui.QAction("Menu", self)
        menuActionMenu.setStatusTip("Add menu")
        
        # Item
        menuActionItem = QtGui.QAction("Item", self)
        menuActionItem.setStatusTip("Add item")
        
        # Separator
        menuActionSeparator = QtGui.QAction("Separator", self)
        menuActionSeparator.setStatusTip("Add separator")

        # Link
        menuActionLink = QtGui.QAction("Link", self)
        menuActionLink.setStatusTip("Add link")

        # Pipemenu
        menuActionPipe = QtGui.QAction("Pipemenu", self)
        menuActionPipe.setStatusTip("Add pipemenu")

        menuAdd = menu.addMenu("&Add")
        menuAdd.addAction(menuActionMenu)
        menuAdd.addAction(menuActionItem)
        menuAdd.addAction(menuActionSeparator)
        menuAdd.addAction(menuActionPipe)
        menuAdd.addAction(menuActionLink)

        # --- Help Menu ---

        # About
        menuActionAbout = QtGui.QAction("About", self)
        menuActionAbout.setStatusTip("About")        

        menuHelp = menu.addMenu("&Help")
        menuHelp.addAction(menuActionAbout)
