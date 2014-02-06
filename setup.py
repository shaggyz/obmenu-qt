#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='obmenu-1.0',
    version='1.0.0',
    packages=find_packages("."),
    package_dir={"", "ob_menu_qt"},
    url='https://github.com/shaggyz/obmenu-qt',
    license='GPL v2',
    author='Nicolás Daniel Palumbo',
    author_email='n@xinax.net',
    description='Simple menu editor for openbox desktop manager'
)
