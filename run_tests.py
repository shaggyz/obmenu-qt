#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
 
if __name__ == "__main__":
    all_tests = unittest.TestLoader().discover('ob_menu_qt/tests', pattern='test_*.py')
    unittest.TextTestRunner().run(all_tests)