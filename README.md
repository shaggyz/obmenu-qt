Openbox menu editor
===================

![Image](../master/doc/snapshot.png?raw=true)

Description:
------------

Obmenu-qt is an Openbox menu editor, written in python and Qt libraries. It allows to edit menus
in an intuitive way. It was inspired (and forked in first instance, but was rewritten from scratch finally)
on another very popular menu editor: http://obmenu.sourceforge.net


Installation:
-------------

Install on the system, requires root privileges (recommended):

<code>$ sudo python setup.py install</code>

Install for the current user only:

<code>$ python setup.py --local install</code>


Requirements:
-------------

- python >= 2.3
- python-qt >= 4
- python-lxml


Usage:
------

Once installation finishes, the **obmenu-qt** executable should be in a system path like /usr/local/bin
and can be started from any terminal:

<code>$ obmenu-qt</code>


To do / Changes / Known issues:
----------------------

The development still active there are a few features not yet implemented:

- [X] Installation script
- [ ] Move up-down from a submenu to another submenu
- [ ] Debian package
- [ ] Open menu file vie menu
- [ ] Save as.. a menu file via menu
- [ ] New menu file vie menu

If you find an error/bug (for sure) on this program please report it on github project site:
https://github.com/shaggyz/obmenu-qt (in the issue tracker)



