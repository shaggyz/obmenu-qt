#!/usr/bin/env python3

from ob_menu.menu import OpenBoxMenu
from ob_menu.gui import Application

menu = OpenBoxMenu()
menu.parse()
menu.dump()

Application.start()
