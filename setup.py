#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='obmenu-qt',
    version='1.0.0',
    packages=['ob_menu_qt', 'ob_menu_qt.ui', 'ob_menu_qt.lib'],
    url='https://github.com/shaggyz/obmenu-qt',
    license='GPL v2',
    author='Nicolás Daniel Palumbo',
    author_email='n@xinax.net',
    description='Simple menu editor for openbox desktop manager',
    entry_points = {
        'gui_scripts': ['obmenu-qt=ob_menu_qt.ob_menu_qt:main'],
        },
    zip_safe=False,
    include_package_data=True,
)
