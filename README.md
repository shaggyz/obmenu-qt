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

- python-setuptools
- python-qt4
- python-lxml


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
- [ ] Port to python3 and Qt5
- [ ] Pipe-menus
- [ ] Links on menu
- [ ] Locale / Internationalization
- [ ] Debian package

If you find an error/bug (for sure) on this program please report it on github project site:
https://github.com/shaggyz/obmenu-qt (in the issue tracker)



