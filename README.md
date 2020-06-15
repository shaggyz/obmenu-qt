Openbox menu editor
===================

![Image](../master/doc/snapshot.png?raw=true)

Description:
------------

Obmenu-qt is an Openbox menu editor, written in python and using the Qt libraries. It allows to edit menus
in an intuitive way. It was inspired on another very popular menu editor: http://obmenu.sourceforge.net


Requirements:
-------------

The best way to install this requirements is through a
package manager like: apt-get, emerge, rpm, yum, etc.

On Debian systems all dependencies can be installed through apt-get:

- python3-setuptools
- python3-pyqt5
- python3-lxml


Installation:
-------------

Install on the system, requires root privileges (recommended):

<code>$ sudo python setup.py install</code>

Install for the current user only:

<code>$ python setup.py --local install</code>


Usage:
------

Once installation finishes, the **obmenu-qt** executable should be in a system path like /usr/local/bin
and can be started from any terminal:

<code>$ obmenu-qt</code>


To do / Changes / Known issues:
----------------------

The development still active there are a few features not yet implemented:

- [X] Installation script
- [X] Move up-down from a submenu to another submenu
- [X] Prompt messages should be able to be edited
- [X] Check if xml loaded file is a openbox menu configuration file
- [X] Open menu file via menu
- [X] Save as.. a menu file via menu
- [X] New menu file via menu
- [X] Port to python3 and Qt5
- [ ] Refactor the whole thing.
- [ ] Pipe-menus?
- [ ] Links on menu?
- [ ] Debian package

> 7 years later note: I just ported this to python3 and Qt5, and... OMG this needs a major refactor :poop:



